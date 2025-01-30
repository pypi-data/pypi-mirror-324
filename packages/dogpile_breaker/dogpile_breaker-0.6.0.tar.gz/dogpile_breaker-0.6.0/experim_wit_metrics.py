import asyncio
import json

from fastapi import FastAPI
from prometheus_async.aio.web import start_http_server

from contextlib import asynccontextmanager
from dogpile_breaker import CacheRegion
from dogpile_breaker.backends.redis_backend import RedisStorageBackend
from dogpile_breaker.middlewares.prometheus_middleware import PrometheusMiddleware

resolve_url_cache = CacheRegion(
    serializer=lambda x: json.dumps(x).encode("utf-8"),
    deserializer=lambda x: json.loads(x.decode("utf-8")),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await resolve_url_cache.configure(
        backend_class=RedisStorageBackend,
        backend_arguments={"host": "localhost", "port": 6379, "max_connections": 100},
        middlewares=[PrometheusMiddleware(region_name="resolve-url")],
    )

    metrics_server = asyncio.create_task(start_http_server(port=9025, addr="0.0.0.0"))
    yield
    metrics_server.cancel()
    await metrics_server


app = FastAPI(lifespan=lifespan)


@resolve_url_cache.cache_on_arguments(
    ttl_sec=10,
    lock_period_sec=2,
    function_key_generator=lambda fn, *args, **kwargs: f"cacke-key:{args[0]}",
)
async def important_function(sleep_for: int | float) -> dict[str, str]:
    await asyncio.sleep(sleep_for)
    return {"status": "OK", "slept": str(sleep_for)}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/sleep")
async def sleep(sleep_for: int | float):
    result = await important_function(sleep_for)
    return result
