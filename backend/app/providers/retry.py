from collections.abc import Awaitable, Callable
from typing import TypeVar

import anyio

T = TypeVar("T")


async def with_retry(
    fn: Callable[[], Awaitable[T]],
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff: float = 2.0,
    retryable: Callable[[Exception], bool] | None = None,
) -> T:
    if retryable is None:
        retryable = lambda e: True

    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return await fn()
        except Exception as e:
            last_exc = e
            if not retryable(e) or attempt == max_retries:
                raise
            delay = base_delay * (backoff ** attempt)
            await anyio.sleep(delay)

    raise last_exc  # type: ignore[misc]
