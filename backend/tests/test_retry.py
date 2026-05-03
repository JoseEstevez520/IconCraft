import pytest

from app.providers.retry import with_retry


class TestRetry:
    @pytest.mark.anyio
    async def test_success_on_first_try(self):
        calls = 0

        async def fn():
            nonlocal calls
            calls += 1
            return "ok"

        result = await with_retry(fn, max_retries=3)
        assert result == "ok"
        assert calls == 1

    @pytest.mark.anyio
    async def test_retries_then_succeeds(self):
        calls = 0

        async def fn():
            nonlocal calls
            calls += 1
            if calls < 3:
                raise TimeoutError("timeout")
            return "ok"

        result = await with_retry(fn, max_retries=3, base_delay=0.01)
        assert result == "ok"
        assert calls == 3

    @pytest.mark.anyio
    async def test_fails_after_max_retries(self):
        calls = 0

        async def fn():
            nonlocal calls
            calls += 1
            raise ValueError("persistent")

        with pytest.raises(ValueError, match="persistent"):
            await with_retry(fn, max_retries=2, base_delay=0.01)
        assert calls == 3

    @pytest.mark.anyio
    async def test_retryable_filter(self):
        calls = 0

        async def fn():
            nonlocal calls
            calls += 1
            raise ValueError("skip")

        with pytest.raises(ValueError):
            await with_retry(
                fn,
                max_retries=2,
                base_delay=0.01,
                retryable=lambda e: isinstance(e, TimeoutError),
            )
        assert calls == 1
