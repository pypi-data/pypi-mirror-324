import asyncio
import importlib
import logging
from collections.abc import Sequence
from enum import Enum
from typing import Any, Optional

import nats
from nats.aio import subscription
from nats.errors import BadSubscriptionError
from nats.js import JetStreamContext, api, client
from nats.js.api import StreamConfig
from nats.js.client import DEFAULT_JS_SUB_PENDING_BYTES_LIMIT, DEFAULT_JS_SUB_PENDING_MSGS_LIMIT
from nats.js.errors import NotFoundError

from nats_app.errors import default_error_handler
from nats_app.marshaling import from_bytes, normalize_payload, to_bytes
from nats_app.meta import PullSubscriptionMeta, PushSubscriptionMeta, SubscriptionMeta
from nats_app.middlewares.common import errors_handler, responder
from nats_app.router import NATSRouter

logger = logging.getLogger(__name__)

JS_DENY_CHANGE_PARAMS = ("name", "num_replicas", "sealed")

JS_ALLOWED_CHANGE_PARAMS = (
    "subjects",
    "max_consumers",
    "max_msgs",
    "max_bytes",
    "max_age",
    "storage",
    "retention",
    "discard",
    "max_msg_size",
    "duplicate_window",
    "allow_rollup_hdrs",
    "deny_delete",
    "deny_purge",
)


class NATS(nats.NATS):
    """NATS client is proxy-class with additional features."""

    def __init__(self) -> None:
        super().__init__()
        self._js_pull_subscribers_tasks = set()

    async def push_from_pull_subscribe(self, js, r: PullSubscriptionMeta):
        """Create a pull subscription handler and run it in background."""
        try:
            sub = await js.pull_subscribe(
                subject=r.subject,
                durable=r.durable,
                stream=r.stream,
                config=r.config,
                pending_msgs_limit=r.pending_msgs_limit,
                pending_bytes_limit=r.pending_bytes_limit,
                inbox_prefix=r.inbox_prefix,
            )
            info = await sub.consumer_info()
        except NotFoundError as e:
            raise ValueError(f"stream '{r.stream}' not found") from e

        pull_task = None

        async def _task():
            try:
                while True:
                    try:
                        msgs = await sub.fetch(batch=r.batch, timeout=r.timeout, heartbeat=r.heartbeat)
                        await r.handler(msgs)
                    except TimeoutError:
                        logger.info("pull message timeout")
                        continue
                    except Exception as e:
                        logger.info(f"Process exception: {e}")
                    await asyncio.sleep(1)
            finally:
                if pull_task:
                    self._js_pull_subscribers_tasks.remove(pull_task)
                logger.info(f"stop pull subscription on stream: {info.stream_name} consumer:{info.name}")

        pull_task = asyncio.create_task(_task())
        self._js_pull_subscribers_tasks.add(pull_task)
        logger.info(f"start pull subscription on stream: '{info.stream_name}' consumer: '{info.name}'")

    async def _js_pull_subscriber_stop(self):
        """Stop all pull subscribers background tasks."""
        for task in self._js_pull_subscribers_tasks:
            task.cancel()
        self._js_pull_subscribers_tasks = set()


class NATSApp:
    _connection_kwargs: dict
    _nc: NATS | None = None
    _js: Optional[JetStreamContext] = None
    _js_opts: dict[str, Any] = {}
    _jetstream_configs: list[StreamConfig]
    _push_subscribers: list[SubscriptionMeta]
    _js_push_subscribers: list[PushSubscriptionMeta]
    _subscriptions: list[subscription.Subscription] = []
    _js_pull_subscribers_tasks: set[asyncio.Task] = set()
    middlewares: Optional[list]

    def __init__(
        self,
        servers: Optional[list[str]] = None,
        js_opts: Optional[dict[str, Any]] = None,
        middlewares: Optional[Sequence] = None,
        **kwargs,
    ) -> None:
        """
        Create a new NATSApp instance.
        """
        self._connection_kwargs = kwargs
        if servers:
            self._connection_kwargs["servers"] = servers

        self.middlewares = middlewares or []
        self._jetstream_configs = []
        self._push_subscribers = []
        self._js_push_subscribers = []
        self._js_pull_subscribers = []
        self._subscriptions = []
        self._js_opts = js_opts or {}

        def _error_handler(m, e):
            return self._error_handler(m, e)

        self.middlewares = [
            responder(),
            errors_handler(_error_handler),
        ]
        self.set_error_handler(default_error_handler)

    async def connect(self, **options):
        """Connect to NATS server."""

        async def disconnected_cb():
            logger.info("NATS disconnected")
            await self._js_pull_subscriber_stop()

        async def reconnected_cb():
            logger.info(f"NATS reconnected {self._nc.connected_url.netloc}")
            await self._js_pull_subscribe_all()
            logger.info("NATS resubscribe")

        async def error_cb(e):
            logger.info(f"NATS was an error: {e}")

        async def closed_cb():
            logger.info("NATS connection is closed")

        self._nc = NATS()

        connection_kwargs = self._connection_kwargs.copy()
        connection_kwargs.update(
            {
                "disconnected_cb": disconnected_cb,
                "reconnected_cb": reconnected_cb,
                "error_cb": error_cb,
                "closed_cb": closed_cb,
            }
        )
        connection_kwargs.update(options)

        await self._nc.connect(**connection_kwargs)
        logger.info("Connected to NATS")
        await self._streams_create_or_update()
        await self.subscribe_all()

    def __getattr__(self, name):
        return getattr(self._nc, name)

    @property
    def js(self):
        """Return JetStreamContext instance."""
        if not self._js:
            self._js = self._nc.jetstream(**self._js_opts)
        return self._js

    async def unsubscribe_all(self):
        """Unsubscribe all subscriptions."""
        await self._js_pull_subscriber_stop()
        if self._nc and not self._nc.is_closed:
            for subscriber in self._subscriptions:
                try:
                    if not subscriber._closed:
                        await subscriber.drain()
                    if not subscriber._closed:
                        await subscriber.unsubscribe()
                except BadSubscriptionError as e:
                    raise ValueError(f"nats: invalid subscription: {subscriber.subject}") from e
        self._subscriptions = []

    @classmethod
    def _stream_config_dict(cls, config: StreamConfig) -> dict:
        """Convert StreamConfig to dict with default values."""
        new = {k: v if not isinstance(v, Enum) else v.value for k, v in config.as_dict().items()}
        if new.get("duplicate_window") == 0:
            new["duplicate_window"] = 120000000000  # default value
        return new

    @classmethod
    def _is_equal(cls, exist, new, fields) -> bool:
        """Check if two config are equal."""
        return all([exist.get(n) == new.get(n) for n in fields if new.get(n) is not None])

    @classmethod
    def _get_change_dict(cls, exist, new, fields):
        """Return a dict with changed"""
        return {
            n: {"old": exist.get(n), "new": new.get(n)}
            for n in fields
            if new.get(n) is not None and exist.get(n) != new.get(n)
        }

    async def _streams_create_or_update(self):
        """Create or update JetStream streams."""
        for config in self._jetstream_configs:
            if config.name is None:
                raise ValueError("nats: stream name is required")
            try:
                si = await self.js.stream_info(config.name)
                exist = self._stream_config_dict(si.config)
                new = self._stream_config_dict(config)

                if not self._is_equal(exist, new, JS_DENY_CHANGE_PARAMS):
                    change = self._get_change_dict(exist, new, JS_DENY_CHANGE_PARAMS)
                    logger.error(f"deny update stream {change}")
                    raise ValueError(f"nats: stream config params {JS_DENY_CHANGE_PARAMS} deny change")

                if not self._is_equal(exist, new, JS_ALLOWED_CHANGE_PARAMS):
                    change = self._get_change_dict(exist, new, JS_ALLOWED_CHANGE_PARAMS)
                    si = await self.js.update_stream(config)
                    logger.info(f"update stream {change} after stream info: {si.as_dict()}")
                else:
                    logger.info(f"unchanged stream: {config.name}")

            except NotFoundError:
                si = await self.js.add_stream(config)
                logger.info(f"add stream info: {si.as_dict()}")

    async def _js_pull_subscribe_all(self):
        """Subscribe all jetstream pull subscribers."""
        for r in self._js_pull_subscribers:
            await self._register_js_pull_subscriber(r)

    async def subscribe_all(self):
        """Subscribe all subscribers."""
        for r in self._push_subscribers:
            await self._register_handler(r)

        for r in self._js_push_subscribers:
            await self._register_js_push_subscriber(r)

        await self._js_pull_subscribe_all()

    async def close(self):
        """Close NATS connection."""
        await self.unsubscribe_all()

        if self._nc and not self._nc.is_closed:
            await self._nc.drain()
        if self._nc and not self._nc.is_closed:
            await self._nc.flush()
        if self._nc and not self._nc.is_closed:
            await self._nc.close()
        self._js = None

    def set_error_handler(self, fn):
        """Set error handler."""
        self._error_handler = fn  # noqa

    def add_middlewares(self, middlewares):
        """Add NATS App middlewares."""
        for m in middlewares:
            if isinstance(m, str):
                try:
                    mod, name = m.rsplit(".", 1)
                    mod = importlib.import_module(mod)
                    m = getattr(mod, name)
                except ModuleNotFoundError as e:
                    raise ModuleNotFoundError(f"Module {m} not found") from e
            self.middlewares.append(m)

    async def publish(
        self,
        subject: str,
        payload: Optional[dict] | bytes = None,
        reply: str = "",
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        """Publish a message."""
        if not isinstance(payload, bytes):
            payload = normalize_payload(payload)
            payload = to_bytes(payload)
        await self._nc.publish(subject, payload, reply, headers)

    async def request(
        self,
        subject: str,
        payload: Any,
        timeout: float = 0.5,
        old_style: bool = False,
        headers: Optional[dict[str, Any]] = None,
    ):
        """Send a request."""
        if not isinstance(payload, bytes):
            payload = normalize_payload(payload)
            payload = to_bytes(payload)
        result = await self._nc.request(subject, payload, timeout, old_style, headers)
        if result is not None:
            result = from_bytes(result.data)
        return result

    def push_subscribe(
        self,
        subject,
        queue: str = "",
        future: Optional[asyncio.Future] = None,
        max_msgs: int = 0,
        pending_msgs_limit: int = subscription.DEFAULT_SUB_PENDING_MSGS_LIMIT,
        pending_bytes_limit: int = subscription.DEFAULT_SUB_PENDING_BYTES_LIMIT,
    ):
        """Decorator for push_subscribe handler."""

        def wrapper(fn):
            self._push_subscribers.append(
                SubscriptionMeta(
                    subject=subject,
                    queue=queue,
                    handler=fn,
                    future=future,
                    max_msgs=max_msgs,
                    pending_msgs_limit=pending_msgs_limit,
                    pending_bytes_limit=pending_bytes_limit,
                )
            )

        return wrapper

    def js_push_subscribe(
        self,
        subject: str,
        queue: Optional[str] = None,
        durable: Optional[str] = None,
        stream: Optional[str] = None,
        config: Optional[api.ConsumerConfig] = None,
        manual_ack: bool = False,
        ordered_consumer: bool = False,
        idle_heartbeat: Optional[float] = None,
        flow_control: bool = False,
        pending_msgs_limit: int = client.DEFAULT_JS_SUB_PENDING_MSGS_LIMIT,
        pending_bytes_limit: int = client.DEFAULT_JS_SUB_PENDING_BYTES_LIMIT,
        deliver_policy: Optional[api.DeliverPolicy] = None,
        headers_only: Optional[bool] = None,
        inactive_threshold: Optional[float] = None,
    ):
        """Decorator for jetstream push_subscribe handler."""

        def wrapper(fn):
            self._js_push_subscribers.append(
                PushSubscriptionMeta(
                    subject=subject,
                    queue=queue,
                    cb=fn,
                    durable=durable,
                    stream=stream,
                    config=config,
                    manual_ack=manual_ack,
                    ordered_consumer=ordered_consumer,
                    idle_heartbeat=idle_heartbeat,
                    flow_control=flow_control,
                    pending_msgs_limit=pending_msgs_limit,
                    pending_bytes_limit=pending_bytes_limit,
                    deliver_policy=deliver_policy,
                    headers_only=headers_only,
                    inactive_threshold=inactive_threshold,
                )
            )

        return wrapper

    def js_pull_subscribe(
        self,
        subject: str,
        durable: Optional[str] = None,
        stream: Optional[str] = None,
        config: Optional[api.ConsumerConfig] = None,
        pending_msgs_limit: int = client.DEFAULT_JS_SUB_PENDING_MSGS_LIMIT,
        pending_bytes_limit: int = client.DEFAULT_JS_SUB_PENDING_BYTES_LIMIT,
        inbox_prefix: bytes = api.INBOX_PREFIX,
        batch: int = 1,
        timeout: Optional[float] = None,
        heartbeat: Optional[float] = None,
    ):
        """Decorator for jetstream pull_subscribe handler."""

        def wrapper(fn):
            self._js_pull_subscribers.append(
                PullSubscriptionMeta(
                    handler=fn,
                    subject=subject,
                    durable=durable,
                    stream=stream,
                    config=config,
                    pending_msgs_limit=pending_msgs_limit,
                    pending_bytes_limit=pending_bytes_limit,
                    inbox_prefix=inbox_prefix,
                    batch=batch,
                    timeout=timeout,
                    heartbeat=heartbeat,
                )
            )

        return wrapper

    @property
    def register_routers(self):
        """Register NATSRouter instances."""

        def _fn(obj):
            if isinstance(obj, NATSRouter):
                # push_subscribe RPC handlers
                for r in obj.push_subscribers:
                    self._push_subscribers.append(r)

                for r in obj.js_push_subscribers:
                    self._js_push_subscribers.append(r)

                for r in obj.js_pull_subscribers:
                    self._js_pull_subscribers.append(r)

            elif isinstance(obj, StreamConfig):
                self._jetstream_configs.append(obj)

        return _fn

    async def _register_handler(self, r: SubscriptionMeta):
        """Register push_subscribe handler."""
        handler = r.handler
        for m in reversed(self.middlewares):
            handler = m(handler)

        sub = await self._nc.subscribe(
            r.subject,
            queue=r.queue,
            cb=handler,
            future=r.future,
            max_msgs=r.max_msgs,
            pending_msgs_limit=r.pending_msgs_limit,
            pending_bytes_limit=r.pending_bytes_limit,
        )
        self._subscriptions.append(sub)
        logger.info("NATS push_subscribe handler on subject: %s", r.subject)

    async def _register_js_push_subscriber(self, r: PushSubscriptionMeta):
        """Register jetstream push_subscribe handler."""
        try_connect = 3  # wait nats jetstream started
        while True:
            try:
                sub = await self.js.subscribe(
                    subject=r.subject,
                    queue=r.queue,
                    cb=r.cb,
                    durable=r.durable,
                    stream=r.stream,
                    config=r.config,
                    manual_ack=r.manual_ack,
                    ordered_consumer=r.ordered_consumer,
                    idle_heartbeat=r.idle_heartbeat,
                    flow_control=r.flow_control,
                    pending_msgs_limit=r.pending_msgs_limit,
                    pending_bytes_limit=r.pending_bytes_limit,
                    deliver_policy=r.deliver_policy,
                    headers_only=r.headers_only,
                    inactive_threshold=r.inactive_threshold,
                )
                self._subscriptions.append(sub)
                logger.info("NATS push_subscribe jetstream push handler on subject: %s", r.subject)
                return
            except asyncio.TimeoutError:
                try_connect -= 1
                if try_connect == 0:
                    raise
                logger.info("NATS Connect to nats jetstream timeout. Retry connect.")

    async def _register_js_pull_subscriber(self, r: PullSubscriptionMeta):
        """Register jetstream pull_subscribe handler."""
        if self._nc:
            await self._nc.push_from_pull_subscribe(self.js, r)

    async def _js_pull_subscriber_stop(self):
        """Stop all jetstream pull subscribers."""
        if self._nc:
            await self._nc._js_pull_subscriber_stop()
