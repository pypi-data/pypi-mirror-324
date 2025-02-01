from __future__ import annotations

import atexit
import os
import time
import pickle
from asyncio import iscoroutinefunction,iscoroutine
from collections import defaultdict
from dataclasses import dataclass, field
from functools import wraps
from pathlib import Path
from queue import Queue
from threading import RLock
from types import GenericAlias
import logging
from typing_extensions import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Callable,
    Coroutine,
    Generator,
    Generic,
    Literal,
    NamedTuple,
    ParamSpec,
    Protocol,
    Self,
    Type,
    TypeVar,
    overload,
    Unpack,
)
from itertools import chain
from mbcore.import_utils import smart_import
from mbcore.display import safe_print
from mbcore._typing import dynamic

P = ParamSpec("P")
R = TypeVar("R")
_R = TypeVar("_R")
__R = TypeVar("__R")
AR = AsyncGenerator[None, _R]
GR = Generator[None, _R, None]
CR = Coroutine[None, None, __R]
GenFunc = Callable[P, GR]
Func = Callable[P, R]
CoroFunc = Callable[P, CR]
AsyncGenFunc = Callable[P, AR]
FuncTs = TypeAlias = Func | GenFunc | AsyncGenFunc | CoroFunc

R_co = TypeVar("R_co", covariant=True)

class MBCacheConfig(NamedTuple):
    PATH: Path = Path.home() / ".mb" / "cache" / "cache.pkl"
    TTL: int = int(os.getenv("MB_CACHE_TTL", 60 * 60 * 24 * 7)) # 1 week
    MTIME_AWARE: bool = bool(os.getenv("MB_CACHE_MTIME_AWARE", True))
    MAX_SIZE: int = int(os.getenv("MB_CACHE_SIZE", 5 * 1024 * 1024)) # 5MB



@dataclass
class CacheEntry:
    value: Any | None = None
    ttl: int = -1
    last_accessed: float = 0.0
    last_updated: float = 0.0
    last_missed: float = 0.0
    isgen: bool = False
    iscoro: bool = False
    isagen: bool = False
    key: Hash = field(default=None)



    def __post_init__(self):
        self.last_accessed = time.time()
        self.last_updated = time.time()
        self.last_missed = 0.0
        if hasattr(self.value, '__aiter__'):
            self.isagen = True
            self.value = _AsyncGenProxy(self.key, self.value)
        elif isinstance(self.value, Coroutine):
            self.iscoro = True
        elif isinstance(self.value, Generator):
            self.isgen = True


config = MBCacheConfig()
Hash: TypeAlias = str | bytes | bytearray | int | float | tuple | frozenset | None
_cache: dict[Hash, CacheEntry] = {}
cache_len = _cache.__len__

lock = RLock()
shorthash = 0

def flatten(v):
    """Flatten a nested data structure."""
    if hasattr(v, 'items') and callable(v.items):
        return chain.from_iterable(flatten(x) for x in v.items())
    if hasattr(v, '__iter__') and not isinstance(v, (str, bytes, bytearray)):
        return chain.from_iterable(flatten(x) for x in v)
    return (v,)

@overload
def flatmap(*vs):...
@overload
def flatmap(v):...
@overload
def flatmap(*vs, func):...
@overload
def flatmap(v, func):...
@overload
def flatmap(func, *vs):...
@overload
def flatmap(func, v):...
def flatmap(*vs, func: Callable[[Any], Any] = lambda x: x):
    """Flatten nested structures and apply `func` at the base level."""
    
    if len(vs) == 1 and callable(vs[0]):  
        func, vs = vs[0], ()  # `flatmap(func)` case, no input provided
    
    elif len(vs) > 1 and callable(vs[0]):  
        func, vs = vs[0], vs[1:]  # `flatmap(func, *vs)`, function first
    
    elif not vs:  
        return ()  # Empty input case
    
    return tuple(
        func(v) if not hasattr(v, '__iter__') or isinstance(v, (str, bytes, bytearray))
        else flatmap(*v.values(), func=func) if hasattr(v, 'items') 
        else flatmap(*v, func=func)
        for v in vs
    )

def _make_key(args, kwds):
    """Generate a fully flattened, immutable hashable key for caching."""
    return flatmap(*args,*kwds.items())


def mtime_key(args, kwds):
    """Invalidates cache entries based on file modification time."""
    key = _make_key(args, kwds)

    key = (key, os.stat(key))
    return key


@dataclass
class CacheInfo:
    hits: int = 0
    misses: int = 0
    maxsize: int = 128
    currsize: int = field(init=False)

    def __post_init__(self):
        self.currsize = len(_cache)


class FunctionCacheInfo(NamedTuple):
    kind: Literal["function","coroutine","generator","async_generator"] = "function"
    total: CacheInfo = CacheInfo()
    by_key: dict[str, CacheInfo] = {}
    


class ParentT:
    __class_getitem__ = classmethod(GenericAlias)


class FuncP(Protocol[P, R_co]):
    def __call__(self: FuncP[P,R], *args: P.args, **kwargs: P.kwargs) -> R: ...


class AFuncP(Protocol[P, R_co]):
    async def __call__(self: AFuncP[P,AR[R] | R], *args: P.args, **kwargs: P.kwargs) -> AR[R] | R: ...

class AsyncGenP(Protocol[P, R_co]):
    def __aiter__(self) -> AsyncGenP[P,AR[R]]:...


FuncT = TypeVar("FuncT", bound=FuncP | AFuncP)

_cache_queue: dict[Hash, Queue[AsyncGenerator[None, Any]]] = defaultdict(Queue)


_P = ParamSpec("_P")
_T = TypeVar("_T")
R = TypeVar("R")
_R_co = TypeVar("_R_co", covariant=True)



def _AsyncGenProxy(key, async_gen: AsyncGenerator[None, R]) -> AsyncGenP[_T,AR[R]]:
    class AsyncGenProxy:
        def __init__(self, key, async_gen=None):
            self.key = key
            self.items = None
            _cache_queue[key].put_nowait(async_gen)

        
        async def __aiter__(self):
            if self.items and not hasattr(self.items, '__aiter__'):
                for item in self.items:
                    yield item
                return
            elif self.items:
                async for item in self.items:
                    yield item
                return

            if self.key in _cache_queue:
                self.items = []
                _gen = _cache_queue[self.key].get()
                if hasattr(_gen, '__aiter__'):
                    async for item in _gen:
                        self.items.append(item)
                        yield item
                    return
                for item in _gen:
                    self.items.append(item)
                    yield item
                return
            raise ValueError(f"Invalid async generator: {self.items}")
    return AsyncGenProxy(key, async_gen)


async def make_cache_tree(cache_dict, filepath):
    filepath = Path(str(filepath)).resolve()
    if not filepath.parent.exists():
        filepath.parent.mkdir(parents=True)
        
    print(f"saving {len(cache_dict)} entries to {filepath}")
    # Clean save - no merging
    serializable = {}
    for k, v in cache_dict.items():
        if not isinstance(v, CacheEntry):
                print(f"[ERROR] Bad entry: {k} → {type(v)}, expected {CacheEntry}")
                print(f"v.__class__.__module__ = {v.__class__.__module__}")
                print(f"CacheEntry.__module__ = {CacheEntry.__module__}")
                print(f"v.__class__.__name__ = {v.__class__.__name__}")    # Handle file operations in a context manager 
   
        if isinstance(v, CacheEntry):
            # Only materialize async generators at pickle time
            val = v.value
            if hasattr(val, '__aiter__'):
                val = [x async for x in val]
            
                v.value = val
                v.key = k
                v.isagen = True
            elif hasattr(val, '__await__') or v.iscoro:
                # raise ValueError(f"Cannot pickle coroutine {val}")
                # val = await val
                v.value = val
                v.key = k
                v.iscoro = True
            if iscoroutinefunction(val) or iscoroutine(val):
                v.iscoro = True
            if hasattr(val, 'send'):
                v.value = [x for x in val]
                v.isgen = True
            
            serializable[k] = v
        else:
            raise ValueError(f"Expected CacheEntry, got {type(v)}")
    with open(filepath, 'wb') as f:
        pickle.dump(serializable, f)
    

def isverbose() -> bool:
    import sys
    return any(arg in sys.argv for arg in ("-v", "--verbose","-d", "--debug"))

def isvverbose() -> bool:
    import sys
    return any(arg in sys.argv for arg in ("-vv", "--vverbose","-dd", "--ddebug"))


def make_cache_trees(cache_dict, filepath):
    if not TYPE_CHECKING:
        cast = smart_import("typing.cast")
        asyncio = smart_import("asyncio")
        threading = smart_import("threading")
    else:
        import asyncio

    async def run_make_cache_tree():
        await make_cache_tree(cache_dict, filepath)

    try:
        loop = asyncio.get_running_loop()  # Safer than get_event_loop() in Python 3.10+
        loop.create_task(run_make_cache_tree())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_make_cache_tree())

class cache(defaultdict, Generic[FuncT, P, R]):
    __slots__ = ("_info", "_pending", "func")
    lock = lock
    if not TYPE_CHECKING:
        cast = smart_import("typing.cast")
        asyncio = smart_import("asyncio")
        weakref = smart_import("weakref")
    else:
        import asyncio
        import weakref
        from typing import cast
   

    def __contains__(self, key):
        return _cache.__contains__(key)

    def __getitem__(self, key):
        entry = _cache[key]
        current_time = time.time()
        if current_time - entry.last_updated > entry.ttl:
            del _cache[key]
            raise KeyError(key)

        new_entry = CacheEntry(
            value=entry.value,
            ttl=entry.ttl,
            last_accessed=current_time,
            last_updated=entry.last_updated,
            last_missed=entry.last_missed,
            isgen=entry.isgen,
            isagen=entry.isagen,
            iscoro=entry.iscoro,
            key=key,

        )
        with self.lock:
            _cache[key] = new_entry
        return entry.value
    @property
    def entries(self):
        return _cache

    def __setitem__(self, key, value):
        if not isinstance(value, CacheEntry):
            entry = CacheEntry(
                value=value,
                ttl=config.TTL,
                last_accessed=time.time(),
                last_updated=time.time(),
                last_missed=0.0,
                isagen=hasattr(value, '__aiter__'),
                iscoro=hasattr(value, '__await__'),
                key=key,
            )
        else:
            entry = value
        with self.lock:
            _cache[key] = entry
        self._info.total.currsize = cache_len()

    def __delitem__(self, key):
        del _cache[key]
        self._info.total.currsize  -= 1

    update = _cache.update
    clear = _cache.clear
    keys = _cache.keys
    values = _cache.values
    items = _cache.items
    pop = _cache.pop
    popitem = _cache.popitem
    setdefault = _cache.setdefault
    get = _cache.get
    __len__ = _cache.__len__
    __iter__ = _cache.__iter__

    def hit(self, key: Hash) -> Self:
        """Record that a key was accessed."""
        self._info.by_key.setdefault(key, CacheInfo()).hits += 1
        self._info.total.hits += 1

    def miss(self, key: Hash) -> "Self":
        """Record that a key was missed."""
        self._info.by_key.setdefault(key, CacheInfo()).misses += 1
        self._info.total.misses += 1
        return self

    def record(self, action: "Literal[hit, miss]") -> Self:
        """Record a cache key and value."""
        if action == "hit":
            self._pending.put_nowait(self.hit)
        elif action == "miss":
            self._pending.put_nowait(self.miss)
        return self

    def on(self, key: Hash) -> Type[cache]:
        """Record that a key was accessed."""
        fn, k = self._pending.get_nowait()
        fn(self, k)  # Call the method with self and key
        return self

    @overload
    def cache_info(self, key:None=None) -> FunctionCacheInfo: ...
    @overload
    def cache_info(self, key:str) -> CacheInfo: ...
    @dynamic()
    def cache_info(self_or_cls, key=None) -> FunctionCacheInfo | CacheInfo:

        if key is not None:
            return self_or_cls._info.by_key.get(key)
        return self_or_cls._info


    @overload
    def __new__(cls, func: Callable[P, R]) -> cache[P, R]: ...
    @overload
    def __new__(cls, func: Callable[P,Generator[None,R]]) -> cache[P,Generator[None,R]]: ...
    @overload
    def __new__(cls, **config: Unpack[MBCacheConfig]) -> cache[P, R]: ...
    @overload
    @wraps(MBCacheConfig)
    def __new__(cls, **config: Unpack[MBCacheConfig]) -> cache[P, R]: ...
    def __new__(
        cls, func: Callable[P, R] | Callable[P, AR[R]] | Callable[P, CR[R]] | Callable[P, GR[R]],
    ) -> cache[P, R] | cache[P, GR[R]]:
      
        instance = super().__new__(cls)
        instance.__init__(func)

        instance._info: FunctionCacheInfo = FunctionCacheInfo()
        instance._pending: Queue[Callable[[Type[cache], Hash], Type[cache]]] = Queue()
        return instance

    @overload
    def __init__(self, func: Callable[P, R]) -> None: ...
    @overload
    def __init__(self, func: Callable[P, AR[R]]) -> None: ...
    @overload
    def __init__(self, func: Callable[P, GR[R]]) -> None: ...
    def __init__(self, func: FuncTs) -> None:

        self.func = func
        self._info = FunctionCacheInfo()
        self._pending = Queue()




    @overload
    def __call__(self: Callable[P,R], *args: P.args, **kwargs: P.kwargs) -> R: ...
    @overload
    def __call__(self: Callable[P,AR], *args: P.args, **kwargs: P.kwargs) -> AR[R]: ...
    @overload
    def __call__(self: Callable[P,CR], *args: P.args, **kwargs: P.kwargs) -> R: ...
    @overload
    def __call__(self: Callable[P,GR], *args: P.args, **kwargs: P.kwargs) -> GR[R]: ...

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R | AR[R] | GR[R]:
        key = _make_key((self.func.__name__, *args), kwargs)
        if key in  self:
            self.hit(key)
            return self[key]

        result = self.func(*args, **kwargs)
        self[key] = result
        self.miss(key) 
        return result

    @classmethod
    def clear_cache(cls) -> None:
        import shutil


        try:
            with cls.lock:
                _cache.clear()

            if config.PATH.exists():
                if config.PATH.is_dir():
                    children = list(config.PATH.iterdir())
                    for child in children:
                        if child.is_dir():
                            print(f"Removing {child}")
                            shutil.rmtree(child)
                        else:
                            print(f"Removing {child}")
                            os.remove(child)
                    shutil.rmtree(config.PATH)
                else:
                    os.remove(config.PATH)

        except Exception:
            import traceback
            traceback.print_exc()

    @classmethod
    def clear_all(cls) -> None:
        """Clear the cache registry."""
        _cache.clear()
        cls._pending = Queue()
        cls.clear_cache()

    @classmethod
    def load(cls, path: Path | str = config.PATH) -> None:
        if not isinstance(path, Path):
            path = Path(path)
        if path.exists():
            try:
                with open(path, 'rb') as f:
                    loaded = pickle.load(f)
                    _cache.update(loaded)
            except (EOFError, pickle.UnpicklingError):
                safe_print(f"[WARNING] Corrupted cache file at {path}. Removing and starting fresh.")
                path.unlink()  # Remove corrupted cache file
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            safe_print(f"Cache path {path} does not exist")
        size = sum(os.path.getsize(f) for f in path.glob('**/*') if f.is_file())
        if size > 0 and logging.getLogger().isEnabledFor(logging.DEBUG):
            safe_print(f"Loaded {len(_cache)} entries from {path} ({size / 1e6:.2f}MB)")
        if size > 0:
            safe_print("[yellow] Warning: Cache size is over 5MB. Consider reducing cache size or TTL.\nSee `mb cache --help` for more information.[/yellow]")
        if size > 0:
            safe_print(f"Cache size: {size / 1e6:.2f}MB. (mb cache)")
        if isverbose():
            safe_print(f"Cache size: {size / 1e6:.2f}MB. (mb cache)")
            safe_print(f"Loaded {len(_cache)} entries with last 10 entries: {list(_cache.keys())[-10:]}")



class acache(cache[AsyncGenFunc[P, R], P, R]):
    """Use c-speed lru_cache for cache entries."""

    @overload
    def __call__(self: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R: ...
    @overload
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R | AR[R] | GR[R]:...
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R | AR[R] | GR[R]:
        key = _make_key((self.func.__name__, *args), kwargs)
        if key in self:
            self.hit(key)
            if self.entries[key].isagen and not hasattr(self[key], '__aiter__'):
                return _AsyncGenProxy(key, self[key])
            async def _wrapper():
                return self[key]
            return _wrapper()
                    
        result = self.func(*args, **kwargs)
        if hasattr(result, '__aiter__'):
            result = _AsyncGenProxy(key, result)
            self[key] = result
            self.miss(key)
            return result

        async def _wrapper(*args, **kwargs):
            key = _make_key((self.func.__name__, *args), kwargs)
            if key in self:
                self.hit(key)
                return self[key]
            nonlocal result
            if hasattr(result, '__await__'):
                result = await result
            self[key] = CacheEntry(result, config.TTL, time.time(), time.time(), 0.0, iscoro=True, key=key)
            return result
        self.miss(key)
        return _wrapper(*args, **kwargs)

        

_handlers_registered = False

def _register_handlers():
    global _handlers_registered
    if not _handlers_registered:
        atexit.register(make_cache_trees, _cache, config.PATH)
        _handlers_registered = True

def ensure_handlers(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        _register_handlers()
        return func(*args, **kwargs)
    return wrapper

@ensure_handlers
def init_cache():
    cache.load()



init_cache()

def example():  
    import asyncio
    @acache
    async def afib(n: int) -> int:
        if n < 2:
            return n
        return (await afib(n - 1)) + (await afib(n - 2))

    @acache
    async def ret_tup():
        yield 1
        yield 2
        yield 3
        return
    async def main():
        print(await afib(10))
        async for x in ret_tup():
            print(x)


    asyncio.run(main())

   
if __name__ == "__main__":
    example()
