import asyncio
import time
import pytest
import pytest_asyncio
from mbcore.cache import cache, acache

@cache
def fib(n: int) -> int:
    time.sleep(0.01)
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

@acache
async def afib(n: int) -> int:
    await asyncio.sleep(0.1)
    if n < 2:
        return n
    return (await afib(n - 1)) + (await afib(n - 2))

@acache
async def ret_tup():
    yield 1
    yield 2
    yield 3
    return

@acache
async def unpack_tup():
    result = [x async for x in ret_tup()]
    a, b, c = result
    return a, b, c

@pytest.mark.asyncio
async def test_unpack_tup():
    a, b, c = await unpack_tup()
    assert (a, b, c) == (1, 2, 3)

@pytest.mark.asyncio
async def test_afib():
    result = await afib(10)
    assert result == 55

def test_fib():
    result = fib(100)
    assert result == 354224848179261915075

def test_fib_cache_info():
    fib(100)
    assert fib.cache_info().total.hits > 0

@pytest.mark.asyncio
async def test_afib_cache_info():
    await afib(10)
    assert afib.cache_info().total.hits > 0


if __name__ == "__main__":
    pytest_asyncio.main(["-v", __file__])