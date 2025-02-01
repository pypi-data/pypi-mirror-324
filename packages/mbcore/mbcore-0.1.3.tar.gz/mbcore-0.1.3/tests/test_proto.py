import pytest
import pytest_asyncio
import asyncio
from mbcore.proto import Coroutine, GeneratorType
from typing import Any, TypeAlias

_CoroutineLike: TypeAlias = GeneratorType[Any, None, dict] | Coroutine[str, str, dict]

@pytest_asyncio.fixture
async def coro() -> Coroutine[str, str, dict]:
    class _ProtocolTestCoro(Coroutine[str, str, dict]):
        def __init__(self):
            super().__init__()
            self.yields = []
            self.sends = []
            
        def _handle_yield(self, sent: None) -> str:
            self.yields.append(('yield', sent))
            return None  # Changed from "yield_value" to None
            
        def _handle_send(self, arg: str) -> str:
            self.sends.append(('send', arg))
            self._value = {"final": "value"}
            return None  # Changed from "send_value" to None
    return _ProtocolTestCoro()

@pytest.mark.asyncio
async def test_verify_protocol(coro: Coroutine[str, str, dict]):

    # Test initial state
    assert coro._state == 'INITIAL', f"Expected state 'INITIAL', got {coro._state}"
    assert not coro.closed, "Coroutine should not be closed initially"

    # Test send before starting
    with pytest.raises(TypeError, match="can't send non-None value to a just-started coroutine"):
        coro.send("bad")

    # Manually advance the coroutine
    gen = coro.__await__()
    assert isinstance(gen, GeneratorType), "Expected a Generator from __await__"

    # Verify first future
    f1 = next(gen)
    print("First Future obtained:", f1)
    await asyncio.sleep(0.1)  # Allow the event loop to process the scheduled call
    print("First Future done status:", f1.done())
    assert isinstance(f1, asyncio.Future), "First yielded value should be an asyncio.Future"
    assert f1.done(), "First future should be completed"
    assert f1.result() is None, "First future result should be None"
    assert coro._state == 'RUNNING', f"Expected state 'RUNNING' after first yield, got {coro._state}"

    # Verify second future
    f2 = gen.send(None)  # Should trigger _handle_send
    print("Second Future obtained:", f2)
    await asyncio.sleep(0.1)  # Increased sleep duration to allow set_result to be called
    print("Second Future done status:", f2.done())
    assert isinstance(f2, asyncio.Future), "Second yielded value should be an asyncio.Future"
    assert f2.done(), "Second future should be completed"
    assert f2.result() is None, "Second future result should be None"
    assert coro._state == 'SUSPENDED', f"Expected state 'SUSPENDED' after second yield, got {coro._state}"

    # Complete the coroutine
    try:
        result = gen.send(None)
    except StopIteration as e:
        result = e.value
    assert result == {"final": "value"}, f"Expected {{'final': 'value'}}, got {result}"
    assert coro.closed, "Coroutine should be closed after completion"
    assert coro._state == 'CLOSED', f"Expected state 'CLOSED' after completion, got {coro._state}"

    # Verify call sequence
    assert len(coro.yields) == 1, f"Expected 1 yield, got {len(coro.yields)}"
    assert len(coro.sends) == 1, f"Expected 1 send, got {len(coro.sends)}"
    assert coro.sends[0][0] == 'send', f"Expected first send action to be 'send', got {coro.sends[0][0]}"
    assert coro.yields[0][0] == 'yield', f"Expected first yield action to be 'yield', got {coro.yields[0][0]}"

@pytest.mark.asyncio
async def test_verify_errors():

    class ErrorTestCoro(Coroutine[str, str, dict]):
        def _handle_send(self, value: str) -> str:
            raise ValueError("send_error")

        def _handle_yield(self, sent: None) -> str:
            raise ValueError("yield_error")
    coro = ErrorTestCoro()

    with pytest.raises(ValueError, match="yield_error"):
        await coro

    assert coro.closed, "Coroutine should be closed after exception"
    assert coro._state == 'CLOSED', f"Expected state 'CLOSED' after exception, got {coro._state}"
