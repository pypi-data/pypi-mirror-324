import asyncio
import sys
from abc import abstractmethod
from collections.abc import Awaitable, Generator
from collections.abc import ItemsView as _ItemsView
from collections.abc import (
    KeysView as _KeysView,
)
from collections.abc import (
    ValuesView as _ValuesView,
)
from types import CodeType, FrameType, NoneType, TracebackType

from typing_extensions import (
    AbstractSet,
    Any,
    Generic,
    Literal,
    Protocol,
    Self,
    TypeAlias,
    TypeVar,
    overload,
    runtime_checkable,
)

_T_co = TypeVar("_T_co", covariant=True)
_KT_co = TypeVar("_KT_co", covariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

_YieldT_co = TypeVar("_YieldT_co", covariant=True)
_SendT_contra = TypeVar("_SendT_contra", contravariant=True, default=None)
_ReturnT_co = TypeVar("_ReturnT_co", covariant=True, default=None)

_AwaitableLike: TypeAlias = Generator[Any, None, _T_co] | Awaitable[_T_co]

@runtime_checkable
class Iterable(Protocol[_T_co]):
    @abstractmethod
    def __iter__(self) -> "Iterator[_T_co]": ...

@runtime_checkable
class Iterator(Iterable[_T_co], Protocol[_T_co]):
    @abstractmethod
    def __next__(self) -> _T_co: ...
    def __iter__(self) -> "Iterator[_T_co]": ...

SupportsIter: TypeAlias = Iterable[_T_co] | Iterator[_T_co]
@runtime_checkable
class GeneratorType(Iterator[_YieldT_co], Generic[_YieldT_co, _SendT_contra, _ReturnT_co], Protocol):
    def __next__(self) -> _YieldT_co: ...
    @abstractmethod
    def send(self, value: _SendT_contra, /) -> _YieldT_co: ...
    @overload
    @abstractmethod
    def throw(
        self, typ: type[BaseException], val: BaseException | object = None, tb: TracebackType | None = None, /
    ) -> _YieldT_co: ...
    @overload
    @abstractmethod
    def throw(self, typ: BaseException, val: None = None, tb: TracebackType | None = None, /) -> _YieldT_co: ...
    def close(self) -> None: ...
    def __iter__(self) -> "GeneratorType[_YieldT_co, _SendT_contra, _ReturnT_co]": ...
    @property
    def gi_code(self) -> CodeType: ...
    @property
    def gi_frame(self) -> FrameType: ...
    @property
    def gi_running(self) -> bool: ...
    @property
    def gi_yieldfrom(self) -> "GeneratorType[Any, Any, Any] | None": ...



class SupportsKeysAndGetItem(Protocol[_KT_co, _VT_co]):
    def keys(self: "SupportsKeysAndGetItem[_KT, _VT]", /) -> AbstractSet[_KT]: ...
    def __getitem__(self: "SupportsKeysAndGetItem[_KT, _VT]", key: _KT, /) -> _VT: ...
    def update(self: "SupportsKeysAndGetItem[_KT, _VT]", other: dict[_KT, _VT], /) -> None: ...
    def get(self: "SupportsKeysAndGetItem[_KT, _VT]", key: _KT, default: _VT, /) -> _VT: ...



class SupportsKeysItems(Protocol[_KT_co, _VT_co]):
    def keys(self: "SupportsKeysItems[_KT, _VT]", /) -> AbstractSet[_KT]: ...
    def __getitem__(self: "SupportsKeysItems[_KT, _VT]", key: _KT, /) -> _VT: ...
    def update(self: "SupportsKeysItems[_KT, _VT]", other: dict[_KT, _VT], /) -> None: ...
    def get(self: "SupportsKeysItems[_KT, _VT]", key: _KT, default: _VT, /) -> _VT: ...
    def items(self)->_ItemsView[str,_VT_co]:...
    def values(self)->_ValuesView[_VT_co]:...
    def __iter__(self)->_KeysView[str]:...
    def __contains__(self, x: Any, /) -> bool: ...
    def __next__(self) -> str: ...
    def __len__(self) -> int: ...



class CoroutineType(Protocol[_YieldT_co, _SendT_contra, _ReturnT_co]):
    __name__: str
    __qualname__: str
    @property
    def cr_origin(self) -> tuple[tuple[str, int, str], ...] | None: ...
    if sys.version_info >= (3, 11):
        @property
        def cr_suspended(self) -> bool: ...

    def close(self) -> None: ...
    def __await__(self) -> GeneratorType[Any, NoneType, _ReturnT_co]: ...
    def send(self, arg: _SendT_contra, /) -> _YieldT_co: ...
    @overload
    def throw(
        self, typ: type[BaseException], val: BaseException | object = ..., tb: TracebackType | None = ..., /
    ) -> _YieldT_co: ...
    @overload
    def throw(self, typ: BaseException, val: None = None, tb: TracebackType | None = ..., /) -> _YieldT_co: ...
    if sys.version_info >= (3, 13):
        def __class_getitem__(cls, item: Any, /) -> Any: ...




class Coroutine(CoroutineType[_YieldT_co, _SendT_contra, _ReturnT_co], Generic[_YieldT_co, _SendT_contra, _ReturnT_co]):
    def __init__(self) -> None:
        self.closed = False
        self._value: _ReturnT_co | None = None
        self._last_sent: _SendT_contra | None = None
        self._state: Literal['INITIAL', 'RUNNING', 'SUSPENDED', 'CLOSED'] = 'INITIAL'
        self.__name__ = self.__class__.__name__
        self.__qualname__ = self.__class__.__qualname__
        # Get the creation frame info for debugging
        if hasattr(sys, '_getframe'):
            frame = sys._getframe(1)
            self._cr_origin = ((frame.f_code.co_filename, 
                              frame.f_lineno,
                              frame.f_code.co_name),)
        else:
            self._cr_origin = None
        self._loop = asyncio.get_running_loop()
        self._current_future: asyncio.Future[Any] | None = None

    @property
    def cr_suspended(self) -> bool:
        return self._state == 'SUSPENDED'

    @property 
    def cr_origin(self) -> tuple[tuple[str, int, str], ...] | None:
        """Return a tuple of (filename, line_number, function_name) tuples.

        Provides information where the coroutine was created, or None if
        this info is not available.
        """
        return self._cr_origin

    def __await__(self) -> Generator[asyncio.Future[_YieldT_co], None, _ReturnT_co]:
        if self.closed:
            raise StopIteration(self._value)

        try:
            self._state = 'RUNNING'
            # Handle yield before yielding the future to record the event
            yield_value = self._handle_yield(None)  # Record the yield event
            print("Yielding first Future with result:", yield_value)

            # Create and complete the Future before yielding
            self._current_future = self._loop.create_future()
            self._current_future.set_result(yield_value)  # Complete the future
            yield self._current_future  # Yielding a completed Future
            print("First Future yielded and completed")

            self._state = 'SUSPENDED'

            # Handle send and set result for the next future
            result = self._handle_send(self._last_sent)
            self._current_future = self._loop.create_future()
            self._current_future.set_result(result)  # Set result immediately instead of scheduling
            yield self._current_future  # Yielding a completed Future
            print("Second Future yielded and completed with result:", result)
            
            if self._value is None:
                raise RuntimeError("No return value set")
            return self._value
        finally:
            self._state = 'CLOSED'
            self.closed = True
            print("Coroutine closed")

    def send(self, arg: _SendT_contra, /) -> _YieldT_co:
        if self.closed:
            raise StopIteration(self._value)
        if self._state == 'INITIAL' and arg is not None:
            raise TypeError("can't send non-None value to a just-started coroutine")
        
        self._state = 'RUNNING'
        self._last_sent = arg  # Store sent value
        try:
            result = self._handle_send(arg)
            if self._current_future and not self._current_future.done():
                # Schedule the Future's result to be set asynchronously
                self._loop.call_soon_threadsafe(self._current_future.set_result, result)
            self._state = 'SUSPENDED'
            return result
        except StopIteration as e:
            self._state = 'CLOSED' 
            self.closed = True
            self._value = e.value  # Capture return value from StopIteration
            raise

    def _handle_yield(self, send_value: _SendT_contra | None = None) -> _YieldT_co:
        """Override to control the yielded value."""
        raise NotImplementedError

    def _handle_send(self, arg: _SendT_contra) -> _YieldT_co:
        raise NotImplementedError

    def close(self) -> None:
        self._state = 'CLOSED'
        self.closed = True

    @overload
    def throw(
        self, typ: type[BaseException], val: BaseException | object = None, tb: TracebackType | None = None, /
    ) -> _YieldT_co: ...

    @overload
    def throw(self, typ: BaseException, val: None = None, tb: TracebackType | None = None, /) -> _YieldT_co: ...

    def throw(self, typ: type[BaseException] | BaseException, val: Any = None, tb: TracebackType | None = None, /) -> _YieldT_co:
        if self.closed:
            raise StopIteration(self._value)
        
        self._state = 'RUNNING'
        exc = typ if isinstance(typ, BaseException) else typ(val)
        if tb is not None:
            exc.__traceback__ = tb
        
        self._state = 'CLOSED'
        self.closed = True
        raise exc



_CoroutineLike: TypeAlias = Generator[Any, None, _T_co] | Coroutine[Any, Any, _T_co]
   
class AsyncGeneratorType(Protocol[_YieldT_co, _SendT_contra]):
    @property
    def ag_await(self) -> Awaitable[Any] | None: ...
    __name__: str
    __qualname__: str
    if sys.version_info >= (3, 12):
        @property
        def ag_suspended(self) -> bool: ...

    def __aiter__(self) -> Self: ...
    def __anext__(self) -> CoroutineType[Any, Any, _YieldT_co]: ...
    def asend(self, val: _SendT_contra, /) -> CoroutineType[Any, Any, _YieldT_co]: ...






if __name__ == "__main__":
    import asyncio  # Ensure asyncio is imported

    async def main():
        # Example usage
        class ProtocolTestCoro(Coroutine[str, None, dict]):
            def __init__(self):
                super().__init__()
                self.yields = []
                self.sends = []
                
            def _handle_yield(self, sent: None) -> str:
                self.yields.append(('yield', sent))
                return "yield_value"
                
            def _handle_send(self, arg: None) -> str:
                self.sends.append(('send', arg))
                self._value = {"final": "value"}
                return "send_value"

        coro = ProtocolTestCoro()
        gen = coro.__await__()
        
        try:
            f1 = next(gen)
            print(f"Yielded value: {f1}")
            
            f2 = gen.send(None)
            print(f"Yielded value after send(None): {f2}")
            
            result = gen.send(None)
            print(f"Returned result: {result}")
            
            assert result == {"final": "value"}, f"Expected {{'final': 'value'}}, got {result}"
            assert coro.closed, "Coroutine should be closed after completion"
            assert coro._state == 'CLOSED', f"Expected state 'CLOSED' after completion, got {coro._state}"
            assert len(coro.yields) == 1, f"Expected 1 yield, got {len(coro.yields)}"
            assert len(coro.sends) == 1, f"Expected 1 send, got {len(coro.sends)}"
            assert coro.sends[0][0] == 'send', f"Expected first send action to be 'send', got {coro.sends[0][0]}"
            assert coro.yields[0][0] == 'yield', f"Expected first yield action to be 'yield', got {coro.yields[0][0]}"
            print("All assertions passed!")
        except StopIteration as e:
            print(f"Coroutine completed with return value: {e.value}")
        except Exception as ex:
            print(f"An unexpected exception occurred: {ex}")

    asyncio.run(main())
