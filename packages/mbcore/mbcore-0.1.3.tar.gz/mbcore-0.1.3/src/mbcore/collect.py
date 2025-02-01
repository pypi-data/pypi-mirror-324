from collections.abc import Callable
from functools import partial, reduce
import re
import sys
from collections import defaultdict, deque
from copy import copy
from datetime import datetime, timedelta
from itertools import (
    accumulate,
    chain,
    count,
    filterfalse,
    groupby,
    islice,
    repeat,
    tee,
)
from itertools import (
    dropwhile as _dropwhile,
)
from itertools import (
    takewhile as _takewhile,
)
from operator import add, attrgetter, itemgetter, methodcaller, not_
from re import Pattern
from time import time
from types import SimpleNamespace, NoneType

from mbcore.more import locate as mlocate, take
from mbcore.more import replace as mreplace
from mbcore.more import seekable as mseekable
from mbcore.more import spy as mspy
from mbcore.more import collapse
from typing_extensions import (
    Any,
    Dict,
    List,
    Literal,
    Mapping,
    ParamSpec,
    Self,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    cast,
    overload,
    Concatenate,
    Generic,
    Protocol,
    runtime_checkable
)
from typing import TYPE_CHECKING

from mbcore.proto import _YieldT_co,SupportsKeysItems,AsyncGeneratorType,GeneratorType,CoroutineType,Iterable,Iterator,SupportsIter

_filter= filter
_map = map
now = datetime.now


class Empty(Iterator):
    def __next__(self) -> Any:
        return None

    def __new__(cls):
        try:
            return cls._instance
        except AttributeError:
            cls._instance = super().__new__(cls)
            return cls._instance

    def __bool__(self):
        return False

    def __repr__(self):
        return "EMPTY"

    def __str__(self):
        return "EMPTY"

    def __lt__(self, other):
        return True

    def __le__(self, other):
        return True

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return other is self

    def __eq__(self, other):
        return other is self

    def __ne__(self, other):
        return other is not self


EMPTY = Empty()

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_S = TypeVar("_S")
_PWrapped = ParamSpec("_PWrapped")
_RWrapped = TypeVar("_RWrapped")
_PWrapper = ParamSpec("_PWrapper")
_RWrapper = TypeVar("_RWrapper")



class namespace(SimpleNamespace):  # noqa
    def __getitem__(self, key):
        if not key.startswith("__"):
            return getattr(self, key)
        raise KeyError(key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __call__(self, *args, **kwargs):
        return namespace(*args, **kwargs)

    def __init__(self, **kwargs: SupportsKeysItems | Dict[str, Any]):
        super().__init__(**kwargs)

_R = TypeVar("_R")


P = ParamSpec("P")
R = TypeVar("R")


WRAPPER_UPDATES = ("__dict__",)
if sys.version_info >= (3, 12):
    WRAPPER_ASSIGNMENTS: tuple[
        Literal["__module__"],
        Literal["__name__"],
        Literal["__qualname__"],
        Literal["__doc__"],
        Literal["__annotations__"],
        Literal["__type_params__"],
    ] = (
        "__module__",
        "__name__",
        "__qualname__",
        "__doc__",
        "__annotations__",
        "__type_params__",
    )
else:
    WRAPPER_ASSIGNMENTS: tuple[
        Literal["__module__"],
        Literal["__name__"],
        Literal["__qualname__"],
        Literal["__doc__"],
        Literal["__annotations__"],
    ] = (
        "__module__",
        "__name__",
        "__qualname__",
        "__doc__",
        "__annotations__",
    )

class _SupportsNext(Protocol[_T_co]):
    def __next__(self) -> _T_co: ...


_SupportsNextT = TypeVar("_SupportsNextT", bound=_SupportsNext)




def first_remaining(iterable: SupportsIter[_SupportsNextT]) -> tuple[_SupportsNextT, Iterator[_SupportsNextT]]:
    """Return the first item and the remaining iterator."""
    iterator = iter(iterable)
    first_item = next(iterator)
    return first_item, iterator

def safe_first(iterable: SupportsIter[_SupportsNextT],default=None) -> _SupportsNextT | None:
    """Return the first item in an iterable or None if it's empty."""
    return first(iterable, default)

def safe_second(iterable: SupportsIter[_SupportsNextT]) -> _SupportsNextT | None:
    """Return the second item in an iterable or None if it's empty."""
    try:
        iterator = iter(iterable)
        next(iterator)
        return next(iterator)
    except StopIteration:
        return None



class NotGivenType:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


NotGivenType.__str__ = lambda self: "..."  # noqa: ARG005
NotGivenType.__repr__ = lambda self: "..."  # noqa: ARG005
NotGiven = NotGivenType()

@overload
def isgiven(value:"EllipsisType | PydanticUndefinedType | Literal['MISSING']" ) -> Literal[False]:...
@overload
def isgiven(value: "_MISSING_TYPE | Literal[_MISSING_TYPE.MISSING] | Literal['_MISSING_TYPE.MISSING']" ) -> Literal[False]:...
@overload
def isgiven(value: Any):...
def isgiven(value: Any):
    return value is not NotGiven and value is not ... and value is not MISSING and value is not NotGivenType and value is not PydanticUndefined and not isinstance(value, _MISSING_TYPE)

@overload
def isnotgiven(value:"NotGivenType | EllipsisType | PydanticUndefinedType | Literal['MISSING']" ) -> Literal[True]:...
@overload
def isnotgiven(value: Any) -> bool:...
def isnotgiven(value: Any) -> bool:
    return value is NotGiven or value is ... or value is MISSING or value is PydanticUndefined
@overload
def exists(value: "NoneType | NotGivenType | EllipsisType | PydanticUndefinedType | Literal['MISSING']") -> Literal[False]:...
@overload
def exists(value: Any):...
def exists(value: Any):
    """Not missing, not None, not NotGiven, not Any, not ..."""
    return value is not None and isgiven(value) and value != Any

P = ParamSpec("P")
V = TypeVar("V")
U = TypeVar("U")
T = TypeVar("T")
R = TypeVar("R")

WRAPPER_ASSIGNMENTS = (
    "__module__",
    "__name__",
    "__qualname__",
    "__doc__",
    "__annotations__",
)
WRAPPER_UPDATES = ("__dict__",)

T = TypeVar("T")
P = ParamSpec("P")


def f(*args: P.args, **kwargs: P.kwargs) -> T: ...


def identity(f: Callable[P, T]) -> Callable[P, T]:
    return f


_P = ParamSpec("_P")
_T = TypeVar("_T",bound="InstanceOf[Any]")


def update_wrapper(
    wrapper=identity,
    wrapped=Callable[...,Any],
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
) -> "Callable[..., InstanceOf[Any]]":
    """Update a wrapper function to look like the wrapped function.

    wrapper is the function to be updated
    wrapped is the original function
    assigned is a tuple naming the attributes assigned directly
    from the wrapped function to the wrapper function (defaults to
    functools.WRAPPER_ASSIGNMENTS)
    updated is a tuple naming the attributes of the wrapper that
    are updated with the corresponding attribute from the wrapped
    function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper


R = TypeVar("R")
_R_co = TypeVar("_R_co", covariant=True)
class dynamic(Generic[_T, _P, _R_co]): # type: ignore # noqa
    """A descriptor that can be used as both a classmethod and instance method.

    Usage:
    ```python
    class MyClass:
        @dynamic()
        def my_method(self_or_cls, arg1, arg2):
            if self_or_cls is MyClass:
                print("Called as class method")
            else:
                print("Called as instance method")
        
        @dynamic
        def my_property(self_or_cls):
            if self_or_cls is MyClass:
                print("Class property")
            else:
                print("Instance property")

    >>> MyClass.my_method(1, 2)
    Called as class method
    >>> MyClass().my_method(1, 2)
    Called as instance method
    >>> MyClass.my_property
    'Class property'
    >>> MyClass().my_property
    'Instance property'
    ```
    """
    def __call__(self, wrapped: Callable[Concatenate[Type[_T],_P], _R_co] | Callable[Concatenate[_T, _P], _R_co]) -> "Callable[_P, _R_co]":
        """Dynamic member access. Use @dynamic for methods and @dynamic() for properties.
         
           Note that properties will return the same class-level object for all instances.
        """
        if wrapped is None:
            raise ValueError("Must provide a callable to @dynamic()")
        if first(inspect.signature(wrapped).parameters) != "self_or_cls":
            raise ValueError("First argument must be 'self_or_cls'." + f" Got {first(inspect.signature(wrapped).parameters)}")
        self.__prop__ = wrapped
        self.__name__ = wrapped.__name__
        self.__qualname__ = wrapped.__qualname__
        self.__doc__ = wrapped.__doc__ 
        self.__module__ = wrapped.__module__
        self.__wrapped__ = wrapped
        self.__func__ = wrapped
        self.__isabstractmethod__ = bool(getattr(wrapped, "__isabstractmethod__", False))
        self._property = False

        return cast(Callable[_P, _R_co], self)


    def __init__(self, f: Callable[Concatenate[type[_T] | _T, _P], _R_co] | None = None, /) -> None:
        if f is None:
            # Dispatch to __call__ to allow for @dynamic() syntax
            return
        if first(inspect.signature(f).parameters) != "self_or_cls":
            raise ValueError("First argument must be 'self_or_cls'." + f" Got {first(inspect.signature(f).parameters)}")
        self.__func__ = f
        self.__name__ = f.__name__
        self.__qualname__ = f.__qualname__
        self.__doc__ = f.__doc__
        self.__module__ = f.__module__
        self.__wrapped__ = f
        self.__isabstractmethod__ = bool(getattr(f, "__isabstractmethod__", False))
        self._property = True

    @overload
    def __get__(self, instance: _T , owner: type[_T]) -> _R_co: ...
    @overload
    def __get__(self, instance: None, owner: type[_T]) -> _R_co:...
    def __get__(self, instance: _T | None, owner: type[_T] | None = None) -> _R_co:
        if self._property:
            if instance is None:
                return self.__func__.__get__(owner, owner.__class__)()
            
            return self.__func__.__get__(instance, owner.__class__)()
        
        if instance is None:
            return self.__func__.__get__(owner, owner.__class__)
        return self.__func__.__get__(instance, owner)
  

Q = ParamSpec("Q")

@overload
def wrapcat(
    wrapped: Callable[Concatenate[V, P], Any],
    ret: type[T] = type[Any],
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
) -> Callable[[Callable[Concatenate[U,Q], T]],Callable[Concatenate[V, U, P], T]]: ...

@overload
def wrapcat(
    wrapped: Callable[Concatenate[V, P], Any],
    ret: type[T] = type[Any],
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
) -> Callable[[Callable[Concatenate[U, Q], T]],Callable[Concatenate[V, U, P], T]]: ...
@overload
def wrapcat(
    wrapped: Callable[Concatenate[V, P], Any],
    ret: type[T] = type[Any],
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
) -> Callable[[Callable[Concatenate[U, Q], T]],Callable[Concatenate[V, U, Q], T]]: ...
@overload
def wrapcat(
    wrapped: Callable[Concatenate[V, P], T],
    ret=None,
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
) -> Callable[[Callable[Concatenate[U, Q], Any]],Callable[Concatenate[V, U, Q], T]]: ...

def wrapcat(
    wrapped,
    ret=None,
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
):
    """Decorator factory to apply update_wrapper() to a wrapper function.

    Returns a decorator that invokes update_wrapper() with the decorated
    function as the wrapper argument and the arguments to wraps() as the
    remaining arguments. Default arguments are as for update_wrapper().
    This is a convenience function to simplify applying partial() to
    update_wrapper().
    """
    ret = ret or [Any]

    uw = cast(Callable[..., Callable[...,Any]], update_wrapper)
    return cast(function,partial(uw, wrapped=wrapped, assigned=assigned, updated=updated))

try:
    from builtins import function
except Exception:
    from types import FunctionType as function

_R_co = TypeVar("_R_co", covariant=True)
@overload
def wraps(
    wrapped: Callable[P, T],
    returns:None=None,
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
) -> Callable[..., Callable[P, T]]:...
@overload
def wraps(
    wrapped: Callable[P, T],
    returns: type[R] = type[Any],
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
) -> Callable[..., Callable[P, R]]:...
@overload
def wraps(
    wrapped: Callable[P, T],
    returns: Any = Any,
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
) -> Callable[..., Callable[P, R]]:...
def wraps(
        wrapped,
        returns: type[Any] | None = None,
        assigned=WRAPPER_ASSIGNMENTS,
        updated=WRAPPER_UPDATES,
):  
    """Decorator factory to apply update_wrapper() to a wrapper function."""
    returns = returns or Any | None
    uw = cast(Callable[..., Callable[...,Any]], update_wrapper)
    return cast(function,partial(uw, wrapped=wrapped, assigned=assigned, updated=updated))


@overload
def wrapafter(
    wrapped: Callable[Concatenate[V, P], U],
    returns:None=None,
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
) -> Callable[[Callable[..., Any]],Callable[P,U]]:...
@overload
def wrapafter(
    wrapped: Callable[Concatenate[V, P], U],
    returns: Type[T] = Type[Any],
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
) -> Callable[[Callable[Concatenate[U, Q], Any]],Callable[Concatenate[U,P],T]]:...
@overload
def wrapafter(
    wrapped: Callable[Concatenate[V,P], U],
    returns: Type[T] = Type[Any],
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
) -> Callable[[Callable[Concatenate[U, Q], Any]],Callable[Concatenate[U,P],T]]:...
def wrapafter(
    wrapped,
    returns=None,
    assigned=WRAPPER_ASSIGNMENTS,
    updated=WRAPPER_UPDATES,
):
    """Decorator factory to apply update_wrapper() to a wrapper function.

    Returns a decorator that invokes update_wrapper() with the decorated
    function as the wrapper argument and the arguments to wraps() as the
    remaining arguments. Default arguments are as for update_wrapper().
    This is a convenience function to simplify applying partial() to
    update_wrapper().
    """
    returns = returns or [Any]
    uw = cast(Callable[..., Callable[...,Any]], update_wrapper)
    return cast(function,partial(uw, wrapped=wrapped, assigned=assigned, updated=updated))


if TYPE_CHECKING:
    @runtime_checkable
    class BaseClass(SupportsKeysItems, Iterator,AsyncGeneratorType,GeneratorType,CoroutineType,Protocol[_T]):...
else:
    BaseClass = Generic[_T]

class CollectIterator(BaseClass):
    _iterator: Iterator[_T]
    def __str__(self):
        return str(list(obj for obj in self))

    def __init__(self, iterable):
        super().__init__()
        self._iterator = iter(iterable)

    def __iter__(self):
        return self._iterator

    def __aiter__(self) -> AsyncGeneratorType[Any,_T]:
        for x in self:
            yield x
        

    def __anext__(self) -> CoroutineType[Any, Any, _YieldT_co]: ...

    def __next__(self):
        return next(self._iterator)

    def consume(self):
        return type(self)(x for x in self)

    async def aconsume(self):
        return type(self)(x async for x in self)

    def tolist(self):
        return list(self._iterator)

    def keys(self):
        return type(self)(iterkeys(self))

    def values(self):
        return type(self)(itervalues(self))

    def items(self):
        return type(self)(iteritems(self))
        
    def seekable(iterable: Iterable[_T]) -> Iterable[_T]:
        iterable = mseekable(iterable)
        iterable.seek(0)
        return iterable


    def exists(key: str) -> Callable[[str], bool]:
        return lambda e: e is not None and key in e


# def ilen(iterable, consume=True):
#     def _ilen(seq):
#         """Consumes an iterable not reading it into memory; return the number of items.

#         NOTE: implementation borrowed from http://stackoverflow.com/a/15112059/753382
#         """
#         counter = count()
#         deque(zip(seq, counter, strict=False), maxlen=0)  # (consume at C speed)
#         return next(counter)

#     if consume:
#         return _ilen(iterable)
#     _cp, iterable = mspy(iterable, _ilen(mseekable(iterable)))
#     return _ilen(iterable)




def rpartial(func, *args, **kwargs):
    """Partially applies last arguments.

    New keyworded arguments extend and override kwargs.
    """
    return lambda *a, **kw: func(*(a + args), **dict(kwargs, **kw))


# def curry(func, n=EMPTY):
#     """Curries func into a chain of one argument functions."""
#     if n is EMPTY:
#         n = get_spec(func).info.max_n

#     if n <= 1:
#         return func
#     if n == 2:
#         return lambda x: lambda y: func(x, y)
#     return lambda x: curry(partial(func, x), n - 1)


# def rcurry(func, n=EMPTY):
#     """Curries func into a chain of one argument functions.

#     Arguments are passed from right to left.
#     """
#     if n is EMPTY:
#         n = get_spec(func).max_n

#     if n <= 1:
#         return func
#     if n == 2:
#         return lambda x: lambda y: func(y, x)
#     return lambda x: rcurry(rpartial(func, x), n - 1)


# def autocurry(func, n=EMPTY, _spec=None, _args=(), _kwargs=None):
#     """Creates a version of func returning its partial applications
#     until sufficient arguments are passed.
#     """
#     if _kwargs is None:
#         _kwargs = {}
#     spec = _spec or (get_spec(func) if n is EMPTY else Spec(n, set(), n, set(), False))

#     @wraps(func)
#     def autocurried(*a, **kw):
#         args = _args + a
#         kwargs = _kwargs.copy()
#         kwargs.update(kw)

#         if (
#             not spec.varkw
#             and len(args) + len(kwargs) >= spec.max_n
#             or len(args) + len(set(kwargs) & spec.names) >= spec.max_n
#         ):
#             return func(*args, **kwargs)
#         if len(args) + len(set(kwargs) & spec.req_names) >= spec.req_n:
#             try:
#                 return func(*args, **kwargs)
#             except TypeError:
#                 return autocurry(func, _spec=spec, _args=args, _kwargs=kwargs)
#         else:
#             return autocurry(func, _spec=spec, _args=args, _kwargs=kwargs)

#     return autocurried


# def iffy(pred: "Predicate", action: Callable | Empty = EMPTY, default: Callable = identity):
#     """Creates a conditional function that applies different transformations based on a predicate.

#     This function is useful when you need to conditionally transform values in data processing
#     pipelines, similar to a functional if-else statement.

#     Parameters
#     ----------
#     pred : callable or any
#         Predicate function or value to test against. If not callable, will be converted
#         to a predicate using `make_pred`.
#     action : callable, optional
#         Function to apply when predicate is True. If not provided, the predicate becomes
#         the action and a bool predicate is used.
#     default : callable or any, optional
#         Function to apply when predicate is False. If not callable, the value itself is returned.
#         Default is identity function.

#     Returns
#     -------
#     callable
#         A function that takes a value and returns either action(value) or default(value)
#         based on the predicate result.

#     Examples
#     --------
#     >>> is_positive = iffy(lambda x: x > 0, lambda x: 'positive', 'negative')
#     >>> is_positive(5)
#     'positive'
#     >>> is_positive(-3)
#     'negative'

#     >>> remove_nulls = iffy(None, lambda _: None, lambda x: x)
#     >>> remove_nulls(None)
#     None
#     >>> remove_nulls('hello')
#     'hello'

#     >>> double_evens = iffy(lambda x: x % 2 == 0, lambda x: x * 2)
#     >>> double_evens(4)
#     8
#     >>> double_evens(3)
#     3

#     """
#     """Creates a function, which conditionally applies action or default."""
#     if action is EMPTY:
#         return iffy(bool, pred, default)
#     pred = make_pred(pred)
#     action = make_func(action)
#     return lambda v: action(v) if pred(v) else default(v) if callable(default) else default


# class MissingT:
#     pass


# _initial_missing = MissingT()


# def reduce(
#     function: Callable[[_T | Callable[..., _T], _T], _T],
#     sequence: Iterable[Callable[..., _T]] | _T,
#     initial: Any | MissingT = _initial_missing,
# ) -> _T:
#     """`reduce(function, iterable[, initial]) -> value`.

#     Apply a function of two arguments cumulatively to the items of a sequence
#     or iterable, from left to right, so as to reduce the iterable to a single
#     value.  For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
#     ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
#     of the iterable in the calculation, and serves as a default when the
#     iterable is empty.
#     """
#     it = iter(sequence)

#     if initial is _initial_missing:
#         try:
#             value = next(it)
#         except StopIteration:
#             raise TypeError(
#                 "reduce() of empty iterable with no initial value",
#             ) from None
#     elif isinstance(initial, MissingT):
#         raise TypeError("reduce() of empty sequence with no initial value")
#     else:
#         value = initial

#     for element in it:
#         value = function(value, element)

#     return value




# CallableT = TypeVar("CallableT", bound=Callable)


# def decorator(deco: Callable[P, T]) -> Callable[[Callable[P, T]], Callable[P, T]]:
#     """Transform a flat wrapper into decorator.

#     Example:
#         @decorator
#         def func(call, methods, content_type=DEFAULT):  # These are decorator params
#             # Access call arg by name
#             if call.request.method not in methods:
#                 # ...
#             # Decorated functions and all the arguments are accesible as:
#             print(call._func, call_args, call._kwargs)
#             # Finally make a call:
#             return call()

#     """
#     if has_single_arg(deco):
#         return make_decorator(deco)
#     if has_1pos_and_kwonly(deco):
#         # Any arguments after first become decorator arguments
#         # And a decorator with arguments is essentially a decorator fab
#         def decorator_fab(_func=None, *dargs, **dkwargs):  # type: ignore
#             if _func is not None:
#                 return make_decorator(deco, *dargs, **dkwargs)(_func)
#             return make_decorator(deco, *dargs, **dkwargs)
#     else:

#         def decorator_fab(*dargs, **dkwargs):
#             return make_decorator(deco, *dargs, **dkwargs)

#     return wraps(deco)(decorator_fab)

# """Bisection algorithms."""


# def insort_right(a, x, lo=0, hi=None, *, key=None):
#     """Insert item x in list a, and keep it sorted assuming a is sorted.

#     If x is already in a, insert it to the right of the rightmost x.

#     Optional args lo (default 0) and hi (default len(a)) bound the
#     slice of a to be searched.

#     A custom key function can be supplied to customize the sort order.
#     """
#     lo = bisect_right(a, x, lo, hi) if key is None else bisect_right(a, key(x), lo, hi, key=key)
#     a.insert(lo, x)


# def bisect_right(a, x, lo=0, hi=None, *, key=None):
#     """Return the index where to insert item x in list a, assuming a is sorted.

#     The return value i is such that all e in a[:i] have e <= x, and all e in
#     a[i:] have e > x.  So if x already appears in the list, a.insert(i, x) will
#     insert just after the rightmost x already there.

#     Optional args lo (default 0) and hi (default len(a)) bound the
#     slice of a to be searched.

#     A custom key function can be supplied to customize the sort order.
#     """
#     if lo < 0:
#         raise ValueError("lo must be non-negative")
#     if hi is None:
#         hi = len(a)
#     # Note, the comparison uses "<" to match the
#     # __lt__() logic in list.sort() and in heapq.
#     if key is None:
#         while lo < hi:
#             mid = (lo + hi) // 2
#             if x < a[mid]:
#                 hi = mid
#             else:
#                 lo = mid + 1
#     else:
#         while lo < hi:
#             mid = (lo + hi) // 2
#             if x < key(a[mid]):
#                 hi = mid
#             else:
#                 lo = mid + 1
#     return lo


def insort_left(a, x, lo=0, hi=None, *, key=None):
    """Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the left of the leftmost x.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.

    A custom key function can be supplied to customize the sort order.
    """
    lo = bisect_left(a, x, lo, hi) if key is None else bisect_left(a, key(x), lo, hi, key=key)
    a.insert(lo, x)


def bisect_left(a, x, lo=0, hi=None, *, key=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(i, x) will
    insert just before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.

    A custom key function can be supplied to customize the sort order.
    """
    if lo < 0:
        raise ValueError("lo must be non-negative")
    if hi is None:
        hi = len(a)
    # Note, the comparison uses "<" to match the
    # __lt__() logic in list.sort() and in heapq.
    if key is None:
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < x:
                lo = mid + 1
            else:
                hi = mid
    else:
        while lo < hi:
            mid = (lo + hi) // 2
            if key(a[mid]) < x:
                lo = mid + 1
            else:
                hi = mid
    return lo






# ### Error handling utilities


# def raiser(exception_or_class=Exception, *args, **kwargs):
#     """Construct function that raises the given exception with given arguments on any invocation."""
#     if isinstance(exception_or_class, str):
#         exception_or_class = Exception(exception_or_class)

#     def _raiser(*a, **kw):
#         if args or kwargs:
#             raise exception_or_class(*args, **kwargs)
#         raise exception_or_class

#     return _raiser


# # Not using @decorator here for speed,
# # since @ignore and @silent should be used for very simple and fast functions
# def ignore(errors, default=None):
#     """Alters function to ignore given errors, returning default instead."""
#     errors = _ensure_exceptable(errors)

#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 return func(*args, **kwargs)
#             except errors:
#                 return default

#         return wrapper

#     return decorator


# def silent(func):
#     """Alters function to ignore all exceptions."""
#     return ignore(Exception)(func)


# ### Backport of Python 3.7 nullcontext
# try:
#     from contextlib import nullcontext
# except ImportError:

#     class nullcontext:
#         """Context manager that does no additional processing.

#         Used as a stand-in for a normal context manager, when a particular
#         block of code is only sometimes used with a normal context manager:

#         cm = optional_cm if condition else nullcontext()
#         with cm:
#             # Perform operation, using optional_cm if condition is True
#         """

#         def __init__(self, enter_result=None):
#             self.enter_result = enter_result

#         def __enter__(self):
#             return self.enter_result

#         def __exit__(self, *excinfo):
#             pass


# @contextmanager
# def reraise(errors, into):
#     """Reraises errors as other exception."""
#     errors = _ensure_exceptable(errors)
#     try:
#         yield
#     except errors as e:
#         if callable(into) and not _is_exception_type(into):
#             into = into(e)
#         raise into from e


# @decorator
# def retry(call, tries, errors=Exception, timeout=0, filter_errors=None):
#     """Make decorated function retry up to tries times.

#     Retries only on specified errors.
#     Sleeps timeout or timeout(attempt) seconds between tries.
#     """
#     errors = _ensure_exceptable(errors)
#     for attempt in range(tries):
#         try:
#             return call()
#         except errors as e:
#             if not (filter_errors is None or filter_errors(e)):
#                 raise

#             # Reraise error on last attempt
#             if attempt + 1 == tries:
#                 raise
#             timeout_value = timeout(attempt) if callable(timeout) else timeout
#             if timeout_value > 0:
#                 time.sleep(timeout_value)
#     return None


def fallback(*approaches):
    """Try several approaches until one works.

    Each approach has a form of (callable, expected_errors).
    """
    for approach in approaches:
        func, catch = (approach, Exception) if callable(approach) else approach
        catch = _ensure_exceptable(catch)
        try:
            return func()
        except catch:
            pass
    return None

def _is_exception_type(value):
    return isinstance(value, type) and issubclass(value, BaseException)

def _ensure_exceptable(errors):
    """Ensure that errors are passable to except clause.

    I.e. should be BaseException subclass or a tuple.
    """
    return errors if _is_exception_type(errors) else tuple(errors)




class ErrorRateExceededError(Exception):
    pass


def limit_error_rate(fails, timeout, exception=ErrorRateExceededError):
    """If function fails to complete fails times in a row, calls to it will be intercepted for timeout with exception raised instead."""
    if isinstance(timeout, int):
        timeout = timedelta(seconds=timeout)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if wrapper.blocked:
                if now() - wrapper.blocked < timeout:
                    raise exception
                wrapper.blocked = None

            try:
                result = func(*args, **kwargs)
            except:  # noqa
                wrapper.fails += 1
                if wrapper.fails >= fails:
                    wrapper.blocked = now()
                raise
            else:
                wrapper.fails = 0
                return result

        wrapper.fails = 0
        wrapper.blocked = None
        return wrapper

    return decorator


def throttle(period):
    """Allow only one run in a period, the rest is skipped."""
    if isinstance(period, timedelta):
        period = period.total_seconds()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if wrapper.blocked_until and wrapper.blocked_until > now:
                return None
            wrapper.blocked_until = now + period

            return func(*args, **kwargs)

        wrapper.blocked_until = None
        return wrapper

    return decorator


# ### Post processing decorators


# @decorator
# def post_processing(call, func):
#     """Post processes decorated function result with func."""
#     return func(call())


# collecting = post_processing(list)
# collecting.__name__ = "collecting"
# collecting.__doc__ = "Transforms a generator into list returning function."

# post_processes = post_processing


# @decorator
# def joining(call, sep):
#     """Join decorated function results with sep."""
#     return sep.join(map(sep.__class__, call()))





class cached_property:
    """Decorator that converts a method with a single self argument into a property cached on the instance."""

    # NOTE: implementation borrowed from Django.
    # NOTE: we use fget, fset and fdel attributes to mimic @property.
    fset = fdel = None

    def __init__(self, fget):
        self.fget = fget
        self.__doc__ = fget.__doc__

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.fget.__name__] = self.fget(instance)
        return res


class cached_readonly(cached_property):
    """Same as @cached_property, but protected against rewrites."""

    def __set__(self, instance, value):
        raise AttributeError("property is read-only")


def wrap_prop(ctx):
    """Wrap a property accessors with a context manager."""

    def decorator(prop):
        class WrapperProp:
            def __repr__(self):
                return repr(prop)

            def __get__(self, instance, type=None):
                if instance is None:
                    return self

                with ctx:
                    return prop.__get__(instance, type)

            if hasattr(prop, "__set__"):

                def __set__(self, name, value):
                    with ctx:
                        return prop.__set__(name, value)

            if hasattr(prop, "__del__"):

                def __del__(self, name):
                    with ctx:
                        return prop.__del__(name)

        return WrapperProp()

    return decorator



class Predicate(Generic[P, _T]):
    def __init__(self, fn: Callable[P, _T]):
        self.fn = fn

    def __call__(self, *args: P.args, **kwargs: P.kwargs):
        return self.fn(*args, **kwargs)

    def __mul__(self, other: Callable | Self) -> "Callable":
        self.fn = compose(self.fn, other)
        return self

    def __rmul__(self, other: Callable | Self) -> "Callable":
        self.fn = compose(other, self.fn)
        return self

    def __imul__(self, other: Callable | Self) -> "Callable":
        self.fn = compose(self.fn, other)
        return self


def __filterfalse(iterable: Iterable[_T], predicate=None) -> Iterable[_T]:
    if predicate is None:
        predicate = bool
    return (item for item in iterable if not predicate(item))


def _equals(value):
    return lambda x: x == value


def _nonzero(d):
    return {k: v for k, v in d.items() if v}


def _notequals(value):
    return lambda x: x != value


def _isnone(x):
    return x is None


def _notnone(x):
    return x is not None


def _inc(x):
    return x + 1


def _dec(x):
    return x - 1


def _even(x):
    return x % 2 == 0


def _odd(x):
    return x % 2 == 1


IterT = TypeVar("IterT", bound=Iterator)
MappingT = TypeVar("MappingT", bound=Mapping)


@overload
def notnone(d: MappingT) -> MappingT: ...
@overload
def notnone(d: IterT) -> IterT: ...
def notnone(d):
    """Remove None values from mappings or iterables.

    For mappings, removes keys with None values.
    For iterables, removes None elements.
    For other types, returns unchanged.
    """
    if not isinstance(d, (Mapping, Iterator)) or isinstance(d, (str, bytes)):
        return d

    if isinstance(d, Mapping):
        return {k: v for k, v in d.items() if v is not None}

    return type(d)(x for x in d if x is not None) if hasattr(d, "__iter__") else d


filterfalse = Predicate(__filterfalse)
equals = Predicate(_equals)
eq = Predicate(_equals)
nonzero = Predicate(_nonzero)
notequals = Predicate(_notequals)
isnone = Predicate(_isnone)
isnotnone = Predicate(_notnone)
inc = Predicate(_inc)
dec = Predicate(_dec)
even = Predicate(_even)
odd = Predicate(_odd)


# REPR_LEN = 25
# def ljuxt(*fs):
#     """Construct  a juxtaposition of the given functions.

#     Result returns a list of results of fs.
#     """
#     extended_fs = list(map(make_func, fs))
#     return lambda *a, **kw: [f(*a, **kw) for f in extended_fs]


# def juxt(*fs):
#     """Construct a lazy juxtaposition of the given functions.

#     Result returns an iterator of results of fs.
#     """
#     extended_fs = list(map(make_func, fs))
#     return lambda *a, **kw: (f(*a, **kw) for f in extended_fs)


def isa(*types: Type) -> Callable[[Any], bool]:
    """Create a function checking if its argument is of any of given types."""
    return lambda x: isinstance(x, types)


isamapping = isa(Mapping)
isaset = isa(Set)
isaseq = isa(Sequence, Iterable, List, Iterator, Tuple)
isalist = isa(list)
isatuple = isa(tuple)

isa_tuple_or_list = isa(list, tuple)
iscountable = isa(list, tuple, Iterator, range)

iterable = isa(Iterable)
is_iter = isa(Iterator)

def tap(x, label=None):
    """Print x and then returns it."""
    if is_iter(x):
        copy, x = tee(x)
        print(f"{label}: {list(copy)}")
    else:
        print(f"{label}: {x}")
    return x



# _filter = filter


# _map, _filter = map, filter


# def _lmap(f, *seqs):
#     return list(map(f, *seqs))


# def _lfilter(f, seq):
#     return list(filter(f, seq))


# def calling(callable_attr: str, *args, **kwargs):
#     """Create a function calling a method of the object with given args and kwargs."""
#     return lambda obj: getattr(obj, callable_attr)(*args, **kwargs)


# def accessing(attr: str):
#     """Create a function accessing an attribute of the object."""
#     return lambda obj: getattr(obj, attr)


# async def asyncaccessing(attr: str):
#     """Create a function accessing an attribute of the object."""

#     async def _accessing(obj):
#         return await getattr(obj, attr)

#     return _accessing


# accesses = accessing


def repeatedly(f, n:Empty | int =EMPTY):
    """Return Iterator that yields the result of f() endlessly or up to n times.

    Takes a function of no args, presumably with side effects,
    and returns an infinite (or length n) iterator of calls to it.
    """
    _repeat = repeat(None) if n is EMPTY else repeat(None, n)
    return (f() for _ in _repeat)


def iterate(f, x):
    """Return an infinite iterator of `x, f(x), f(f(x)), ...`."""
    while True:
        yield x
        x = f(x)


def take(n, seq):
    """Return  a list of first n items in the sequence, or less if the sequence is shorter."""
    return list(islice(seq, n))


def drop(n, seq):
    """Skips first n items in the sequence, yields the rest."""
    return islice(seq, n, None)





# def has_single_arg(func: Callable):
#     sig = signature(func)
#     if len(sig.parameters) != 1:
#         return False
#     arg = next(iter(sig.parameters.values()))
#     return arg.kind not in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD)


# def has_1pos_and_kwonly(func):
#     from collections import Counter
#     from inspect import Parameter as P

#     sig = signature(func)
#     kinds = Counter(p.kind for p in sig.parameters.values())
#     return kinds[P.POSITIONAL_ONLY] + kinds[P.POSITIONAL_OR_KEYWORD] == 1 and kinds[P.VAR_POSITIONAL] == 0

def _make_getter(regex: Pattern):
    if regex.groups == 0:
        return methodcaller("group")
    if regex.groups == 1 and regex.groupindex == {}:
        return methodcaller("group", 1)
    if regex.groupindex == {}:
        return methodcaller("groups")
    if regex.groups == len(regex.groupindex):
        return methodcaller("groupdict")
    return lambda m: m


# def get_argnames(func: FunctionType) -> Iterable[str]:
#     func = getattr(func, "__original__", None) or unwrap(func)
#     return func.__code__.co_varnames[: func.__code__.co_argcount]

def _prepare(regex, flags):
    if not isinstance(regex, re.Match):
        regex = re.compile(regex, flags)
    return regex, _make_getter(regex)


# def re_iter(regex: Pattern, s, flags=0):
#     """Iterate over matches of regex in s, presents them in simplest possible form."""
#     regex, getter = _prepare(regex, flags)
#     return map(getter, regex.finditer(s))


# def re_all(regex, s, flags=0):
#     """List all matches of regex in s, presents them in simplest possible form."""
#     return list(re_iter(regex, s, flags))


def re_finder(regex, flags=0):
    """Create a function finding regex in passed string."""
    regex, _getter = _prepare(regex, flags)
    getter = lambda m: _getter(m) if m else None
    return lambda s: getter(regex.search(s))


def re_find(regex, s, flags=0):
    """Match regex against the given string, return the match in the simplest possible form."""
    return re_finder(regex, flags)(s)




def str_join(sep, seq=EMPTY):
    """Join the given sequence with sep. Forces stringification of seq items."""
    if seq is EMPTY:
        return str_join("", sep)
    return sep.join(map(sep.__class__, seq))


def cut_prefix(s, prefix):
    """Cuts prefix from given string if it's present."""
    return s[len(prefix) :] if s.startswith(prefix) else s


def cut_suffix(s, suffix):
    """Cuts suffix from given string if it's present."""
    return s[: -len(suffix)] if s.endswith(suffix) else s

def re_tester(regex, flags=0):
    """Create a predicate testing passed string with regex."""
    if not isinstance(regex, re.Match):
        regex = re.compile(regex, flags)
    return lambda s: bool(regex.search(s))


def re_test(regex, s, flags=0):
    """Test whether regex matches against s."""
    return re_tester(regex, flags)(s)



def make_func(f, test=False):
    """Convert various types of inputs into callable functions.

    This utility function creates a callable function from different types of inputs,
    useful for filtering, mapping, and testing operations.

    Args:
        f: Input to be converted to a function. Can be one of:
            - callable: Returns the callable as-is
            - None: Returns bool if test=True, or identity function if test=False
            - str/bytes/regex: Returns regex tester if test=True, or finder if test=False
            - int/slice: Returns an itemgetter function
            - dict-like: Returns the __getitem__ method
            - set-like: Returns the __contains__ method
        test (bool, optional): Flag to modify behavior for None and regex inputs.
            Defaults to False.

    Returns:
        callable: A function that can be used for filtering, mapping or testing.

    Raises:
        TypeError: If the input type cannot be converted to a function.

    Examples:
        >>> make_func(lambda x: x > 5)  # Returns the function as-is
        <function <lambda> at ...>

        >>> make_func(None)  # Returns identity function
        <function <lambda> at ...>

        >>> make_func(None, test=True)  # Returns bool function
        <built-in function bool>

        >>> make_func('pattern')  # Returns regex finder
        <function re_finder at ...>

        >>> make_func('pattern', test=True)  # Returns regex tester
        <function re_tester at ...>

        >>> make_func(2)  # Returns itemgetter(2)
        <operator.itemgetter at ...>

        >>> make_func({'a': 1})  # Returns dict.__getitem__
        <built-in method __getitem__ of dict object at ...>

        >>> make_func({1, 2, 3})  # Returns set.__contains__
        <built-in method __contains__ of set object at ...>

    """
    if callable(f):
        return f
    if f is None:
        # pass None to builtin as predicate or mapping function for speed
        return bool if test else lambda x: x
    if isinstance(f, bytes | str | re.Match):
        return re_tester(f) if test else re_finder(f)
    if isinstance(f, int | slice):
        return itemgetter(f)
    if isinstance(f, Mapping):
        return f.__getitem__
    if isinstance(f, Set):
        return f.__contains__
    raise TypeError(f"Can't make a func from {f.__class__.__name__}")


def make_pred(pred):
    return make_func(pred, test=True)







@overload
def first(coll: Iterable[_T], default: _T | None = None) -> _T: ...
@overload
def first(coll: Sequence[_T], pred: Callable[[_T], bool], default: _T | None = None) -> _T | None: ...
@overload
def first(pred: Callable[[_T], bool], coll: Sequence[_T], default: _T | None = None) -> _T | None: ...
def first(*args, **kwargs):
    """Return the first item in the sequence or the first item passing the predicate.

    Returns None if the sequence is empty.
    """
    pred = kwargs.get("pred", None)
    if len(args) == 1:
        coll, = args
        if pred is None:
            return next(iter(coll), None)
        return next(filter(pred, coll), None)
    if pred is None:
        coll, default = args
        return next(iter(coll), default) 


def second(seq):
    """Return second item in the sequence.

    Return None if there are less than two items in it.
    """
    return first(rest(seq))


def nth(n, seq):
    """Return nth item in the sequence or None if no such item exists."""
    try:
        return seq[n]
    except IndexError:
        return None
    except TypeError:
        return next(islice(seq, n, None), None)


def last(seq):
    """Return the last item in the sequence or iterator.

    Return None if the sequence is empty.
    """
    try:
        return seq[-1]
    except IndexError:
        return None
    except TypeError:
        item = None
        for x in seq:
            item = x
        return item


def rest(seq):
    """Skips first item in the sequence, yields the rest."""
    return drop(1, seq)


def butlast(seq):
    """Iterate over all elements of the sequence but last."""
    it = iter(seq)
    try:
        prev = next(it)
    except StopIteration:
        pass
    else:
        for item in it:
            yield prev
            prev = item




def filter(pred, seq):
    """List filter results.

    Derives a predicate from string, int, slice, dict or set.
    """
    return _filter(make_pred(pred), seq)


def map(f, *seqs):
    """Map each item in the sequence(s) through the function.

    Derives a mapper from string, int, slice, dict or set.

    Example:
        map("name", users)  # Returns a list of names from users

    """
    if ilen(seqs, consume=False) == 1:
        out = _map(make_func(f), seqs[0])
        return collect(out)
    _map(make_func(f), *seqs)
    return (*seqs,)


def lremove(pred, seq):
    """Create a list of items passing given predicate."""
    return list(remove(pred, seq))


def remove(pred, seq):
    """Iterate items passing given predicate."""
    return filterfalse(seq, make_pred(pred))


def lkeep(f, seq=EMPTY):
    """Map seq with f and keeps only truthy results.

    Simply lists truthy values in one argument version.
    """
    return list(keep(f, seq))


def keep(f, seq: Iterable | Empty = EMPTY):
    """Map seq with f and iterate truthy results.

    Simply iterates truthy values in one argument version.
    """
    if seq is EMPTY:
        return _filter(bool, f)
    return _filter(bool, map(f, seq))


def without(seq, *items):
    """Iterate over sequence skipping items."""
    for value in seq:
        if value not in items:
            yield value


def lwithout(seq, *items):
    """Remove items from sequence, preserves order."""
    return list(without(seq, *items))


def lconcat(*seqs):
    """Concatenates several sequences."""
    return list(chain(*seqs))


concat = chain


def lcat(seqs):
    """Concatenates the sequence of sequences."""
    return list(cat(seqs))


cat = chain.from_iterable




def caller(*a, **kw):
    """Create a function calling its sole argument with given *a, **kw."""
    return lambda f: f(*a, **kw)


def partial(func, *args, **kwargs):
    """Return a real partial function.

    Can be used to construct methods.
    """
    if not args:
        return lambda *a, **kw: func(*a, **dict(kwargs, **kw))
    return lambda *a, **kw: func(*(args + a), **dict(kwargs, **kw))


def doesnot(func):
    """Negates the result of the function."""
    return compose(not_, func)

isnot = doesnot
P = ParamSpec("P")
_R = TypeVar("_R")
@overload
def compose(f: Callable[P, _S], /) -> Callable[P, _S]: ...
@overload
def compose(f: Callable[P, _S], g: Callable[[_S], _R], /) -> Callable[P, _R]: ...


def compose(*fs):
    """Composes passed functions."""
    if fs:
        pair = lambda f, g: lambda *a, **kw: f(g(*a, **kw))
        return reduce(pair, map(make_func, fs))

    return identity


@overload
def rcompose(f: Callable[P, _S], /) -> Callable[P, _S]: ...
@overload
def rcompose(f: Callable[P, _S], g: Callable[[_S], _R], /) -> Callable[P, _R]: ...
def rcompose(*fs):
    """Composes functions, calling them from left to right."""
    return compose(*reversed(fs))


# def complement(pred):
#     """Construct a complementary predicate."""
#     return compose(not_, pred)


# # NOTE: using lazy map in these two will result in empty list/iterator
# #       from all calls to i?juxt result since map iterator will be depleted


# def ljuxt(*fs):
#     """Construct  a juxtaposition of the given functions.

#     Result returns a list of results of fs.
#     """
#     extended_fs = list(map(make_func, fs))
#     return lambda *a, **kw: [f(*a, **kw) for f in extended_fs]


# def juxt(*fs):
#     """Construct a lazy juxtaposition of the given functions.

#     Result returns an iterator of results of fs.
#     """
#     extended_fs = list(map(make_func, fs))
#     return lambda *a, **kw: (f(*a, **kw) for f in extended_fs)


def isa(*types: Type) -> Callable[[Any], bool]:
    """Create a function checking if its argument is of any of given types."""
    return lambda x: isinstance(x, types)


isamapping = isa(Mapping)
isaset = isa(Set)
isaseq = isa(Sequence, Iterable, List, Iterator, Tuple)
isalist = isa(list)
isatuple = isa(tuple)

isa_tuple_or_list = isa(list, tuple)
iscountable = isa(list, tuple, Iterator, range)

iterable = isa(Iterable)
is_iter = isa(Iterator)

T = TypeVar("T")
def tree_leaves(root: Iterator[T], follow=iscountable, children=iter) -> Iterator[T] | Iterator[Iterator[T]]:
    """Iterate over tree leaves."""
    q: deque[list[Iterator[T]] | Iterator[Iterator[T]]] = deque([[root]])
    while q:
        node_iter = iter(q.pop())
        for sub in node_iter:
            if follow(sub):
                q.append(node_iter)
                q.append(children(sub))
                break
            else:
                yield sub


def tree_nodes(root: Iterator[T], follow=iscountable, children=iter) -> Iterator[T] | Iterator[Iterator[T]]:
    """Iterates over all tree nodes."""
    q: deque = deque([[root]])
    while q:
        node_iter = iter(q.pop())
        for sub in node_iter:
            yield sub
            if follow(sub):
                q.append(node_iter)
                q.append(children(sub))
                break



def identity(x):
    """Return its argument."""
    return x


def constantly(x):
    """Create a function accepting any args, but always returning x."""


def flatten(seq, follow=iscountable):
    """Flattens arbitrary nested sequence.

    Unpacks an item if follow(item) is truthy.
    """
    for item in seq:
        if follow(item):
            yield from flatten(item, follow)
        else:
            yield item

def lmapcat(f, *seqs):
    """Map given sequence(s) and concatenates the results."""
    return lcat(map(f, *seqs))


def mapcat(f, *seqs):
    """Map given sequence(s) and chains the results."""
    return cat(map(f, *seqs))


def interleave(*seqs):
    """Yield first item of each sequence, then second one and so on."""
    return cat(zip(*seqs, strict=False))


def interpose(sep, seq):
    """Yield items of the sequence alternating with sep."""
    return drop(1, interleave(repeat(sep), seq))


def takewhile(pred, seq=EMPTY):
    """Yield sequence items until first predicate fail.

    Stops on first falsy value in one argument version.
    """
    if seq is EMPTY:
        pred, seq = bool, pred
    else:
        pred = make_pred(pred)
    return _takewhile(pred, seq)


def dropwhile(pred, seq=EMPTY):
    """Skip the start of the sequence passing pred (or just truthy), yield the rest."""
    if seq is EMPTY:
        pred, seq = bool, pred
    else:
        pred = make_pred(pred)
    return _dropwhile(pred, seq)


def ldistinct(seq, key=EMPTY):
    """Remove duplicates from sequences, preserves order."""
    return list(distinct(seq, key))


def distinct(seq, key=EMPTY):
    """Iterate over sequence skipping duplicates."""
    seen = set()
    # check if key is supplied out of loop for efficiency
    if key is EMPTY:
        for item in seq:
            if item not in seen:
                seen.add(item)
                yield item
    else:
        key = make_func(key)
        for item in seq:
            k = key(item)
            if k not in seen:
                seen.add(k)
                yield item


def split(pred, seq):
    """Lazily split items which pass the predicate from the ones that don't.

    Returns a pair (passed, failed) of respective iterators.
    """
    pred = make_pred(pred)
    yes, no = deque(), deque()
    splitter = (yes.append(item) if pred(item) else no.append(item) for item in seq)

    def _split(q):
        while True:
            while q:
                yield q.popleft()
            try:
                next(splitter)
            except StopIteration:
                return

    return _split(yes), _split(no)


def lsplit(pred, seq):
    """Split items which pass the predicate from the ones that don't.

    Returns a pair (passed, failed) of respective lists.
    """
    pred = make_pred(pred)
    yes, no = [], []
    for item in seq:
        if pred(item):
            yes.append(item)
        else:
            no.append(item)
    return yes, no


def split_at(n, seq):
    """Lazily splits the sequence at given position, returning a pair of iterators over its start and tail."""
    a, b = tee(seq)
    return islice(a, n), islice(b, n, None)


def lsplit_at(n, seq):
    """Split the sequence at given position, returning a tuple of its start and tail."""
    a, b = split_at(n, seq)
    return list(a), list(b)


def split_by(pred, seq):
    """Lazily split the start of the sequence, consisting of items passing pred, from the rest of it."""
    a, b = tee(seq)
    return takewhile(pred, a), dropwhile(pred, b)


def group_by(f, seq):
    """Group given sequence items into a mapping f(item) -> [item, ...]."""
    f = make_func(f)
    result = defaultdict(list)
    for item in seq:
        result[f(item)].append(item)
    return result


def group_by_keys(get_keys, seq):
    """Group items having multiple keys into a mapping key -> [item, ...].

    Item might be repeated under several keys.
    """
    get_keys = make_func(get_keys)
    result = defaultdict(list)
    for item in seq:
        for k in get_keys(item):
            result[k].append(item)
    return result


def group_values(seq):
    """Take a sequence of (key, value) pairs and groups values by keys."""
    result = defaultdict(list)
    for key, value in seq:
        result[key].append(value)
    return result


def count_by(f, seq):
    """Count numbers of occurrences of values of f() on elements of given sequence."""
    f = make_func(f)
    result = defaultdict(int)
    for item in seq:
        result[f(item)] += 1
    return result


def count_reps(seq):
    """Count number occurrences of each value in the sequence."""
    result = defaultdict(int)
    for item in seq:
        result[item] += 1
    return result


# For efficiency we use separate implementation for cutting sequences (those capable of slicing)
def _cut_seq(drop_tail, n, step, seq):
    limit = len(seq) - n + 1 if drop_tail else len(seq)
    return (seq[i : i + n] for i in range(0, limit, step))


def _cut_iter(drop_tail, n, step, seq):
    it = iter(seq)
    pool = take(n, it)
    while True:
        if len(pool) < n:
            break
        yield pool
        pool = pool[step:]
        pool.extend(islice(it, step))
    if not drop_tail:
        yield from _cut_seq(drop_tail, n, step, pool)


def _cut(drop_tail, n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step
    if isinstance(seq, Sequence):
        return _cut_seq(drop_tail, n, step, seq)
    return _cut_iter(drop_tail, n, step, seq)


def partition(n, step, seq=EMPTY):
    """Lazily partition seq into parts of length n.

    Skips step items between parts if passed. Non-fitting tail is ignored.
    """
    return _cut(True, n, step, seq)


def lpartition(n, step, seq=EMPTY):
    """Partitions seq into parts of length n.

    Skips step items between parts if passed. Non-fitting tail is ignored.
    """
    return list(partition(n, step, seq))


def chunks(n, step, seq=EMPTY):
    """Lazily chunk seq into parts of length n or less.

    Skips step items between parts if passed.
    """
    return _cut(False, n, step, seq)


def lchunks(n, step, seq=EMPTY):
    """Chunk seq into parts of length n or less.

    Skips step items between parts if passed.
    """
    return list(chunks(n, step, seq))


def partition_by(f, seq):
    """Lazily partition seq into continuous chunks with constant value of f."""
    f = make_func(f)
    for _, items in groupby(seq, f):
        yield items


# def lpartition_by(f, seq):
#     """Partition seq into continuous chunks with constant value of f."""
#     return _lmap(list, partition_by(f, seq))


def with_prev(seq, fill=None):
    """Yield each item paired with its preceding: (item, prev)."""
    a, b = tee(seq)
    return zip(a, chain([fill], b), strict=False)


def with_next(seq, fill=None):
    """Yield each item paired with its following: (item, next)."""
    a, b = tee(seq)
    next(b, None)
    return zip(a, chain(b, [fill]), strict=False)


# An itertools recipe
# NOTE: this is the same as ipartition(2, 1, seq) only faster and with distinct name
def pairwise(seq):
    """Yield all pairs of neighboring items in seq."""
    a, b = tee(seq)
    next(b, None)
    return zip(a, b, strict=False)


def lzip(*seqs, strict=False):
    """List zip() version."""
    return list(zip(*seqs, strict=strict))


def _reductions(f, seq, acc):
    last = acc
    for x in seq:
        last = f(last, x)
        yield last


def reductions(f, seq, acc=EMPTY):
    """Yield intermediate reductions of seq by f."""
    if acc is EMPTY:
        return accumulate(seq) if f is add else accumulate(seq, f)
    return _reductions(f, seq, acc)


# def lreductions(f, seq, acc=EMPTY):
#     """List intermediate reductions of seq by f."""
#     return list(reductions(f, seq, acc))


def sums(seq, acc=EMPTY):
    """Yield partial sums of seq."""
    return reductions(add, seq, acc)


# def lsums(seq, acc=EMPTY):
#     """List partial sums of seq."""
#     return lreductions(add, seq, acc)

def isdistinct(coll, key=EMPTY):
    """Check if all elements in the collection are different."""
    if key is EMPTY:
        return len(coll) == len(set(coll))
    return len(coll) == len(set(xmap(key, coll)))


def all(pred, seq: Iterator = EMPTY):
    """Check if all items in seq pass pred (or are truthy)."""
    if seq is EMPTY:
        return _all(pred)
    return _all(xmap(pred, seq))


def any(pred, seq: Iterator = EMPTY):  # noqa
    """Check if any item in seq passes pred (or is truthy)."""
    if seq is EMPTY:
        return _any(pred)
    return _any(xmap(pred, seq))


def none(pred, seq: Iterator = EMPTY):
    """Check if none of the items in seq pass pred (or are truthy)."""
    return not any(pred, seq)


def one(pred, seq: Iterator = EMPTY):
    """Check whether exactly one item in seq passes pred (or is truthy)."""
    if seq is EMPTY:
        return one(bool, pred)
    return len(take(2, filter(pred, seq))) == 1


# Not same as in clojure! returns value found not pred(value)
def some(pred, seq: Iterator | Empty = EMPTY):
    """Find first item in seq passing pred or first that is truthy."""
    if seq is EMPTY:
        return some(bool, pred)
    return next(filter(pred, seq), None)


def ilen(iterable, consume=True):
    def _ilen(seq):
        """Consumes an iterable not reading it into memory; return the number of items.

        NOTE: implementation borrowed from http://stackoverflow.com/a/15112059/753382
        """
        counter = count()
        deque(zip(seq, counter, strict=False), maxlen=0)  # (consume at C speed)
        return next(counter)

    if consume:
        return _ilen(iterable)
    _cp, iterable = mspy(iterable, _ilen(seekable(iterable)))
    return _ilen(iterable)


def spy(iterable, length: int | None = None) -> Tuple[List[_T], Iterable[_T]]:
    return mspy(iterable, ilen(iterable, consume=False) if length is None else length)


def locate(iterable, pred, window: int | None = None, consume=True):
    if window is not None and window < 1:
        raise ValueError("window size must be at least 1")
    if not consume:
        iterable, copy = spy(iterable)
        return mlocate(copy, pred, window)
    return mlocate(iterable, pred, window)


def zipvalues(*dicts):
    """Yield tuples of corresponding values of several dicts."""
    if len(dicts) < 1:
        raise TypeError("zip_values expects at least one argument")
    keys = set.intersection(*map(set, dicts))
    for key in keys:
        yield tuple(d[key] for d in dicts)


def zipdicts(*dicts):
    """Yield tuples like (key, (val1, val2, ...)) for each common key in all given dicts."""
    if len(dicts) < 1:
        raise TypeError("zip_dicts expects at least one argument")
    keys = set.intersection(*map(set, dicts))
    for key in keys:
        yield key, tuple(d[key] for d in dicts)


def getin(coll: SupportsKeysItems, path: Iterable[str] | str, default=None, delimeter="."):
    """Return a value at path in the given nested collection."""
    return setdefault(coll, path.split(delimeter)[:-1], default, delimeter).get(path.split(delimeter)[-1], default)


def setdefault(coll: SupportsKeysItems, key: str | Iterable[str], default=None, delimeter="."):
    if isinstance(key, str):
        path = key.split(delimeter)
    d = coll if hasattr(coll, "setdefault") else defaultdict(default)
    for key in path:
        d = d.setdefault(key, {})
    coll.update(d) if coll is not d else {}
    return coll


def getlax(coll, path, default=None):
    """Return a value at path in the given nested collection.

    Does not raise on a wrong collection type along the way, but returns default.
    """
    for key in path:
        try:
            coll = coll[key]
        except (KeyError, IndexError, TypeError):
            return default
    return coll


def updatein(coll, path, update, default=None):
    """Create a copy of coll with a value updated at path."""
    if not path:
        return update(coll)
    if isinstance(coll, list):
        copy = coll[:]
        # NOTE: there is no auto-vivication for lists
        copy[path[0]] = updatein(copy[path[0]], path[1:], update, default)
        return copy

    copy = coll.copy()
    current_default = {} if len(path) > 1 else default
    copy[path[0]] = updatein(copy.get(path[0], current_default), path[1:], update, default)
    return copy


def delin(coll, path):
    """Create a copy of coll with a nested key or index deleted."""
    if not path:
        return coll
    try:
        next_coll = coll[path[0]]
    except (KeyError, IndexError):
        return coll

    coll_copy = copy(coll)
    if len(path) == 1:
        del coll_copy[path[0]]
    else:
        coll_copy[path[0]] = delin(next_coll, path[1:])
    return coll_copy


def haspath(coll, path):
    """Check if path exists in the given nested collection."""
    for p in path:
        try:
            coll = coll[p]
        except (KeyError, IndexError):
            return False
    return True



def where(mappings, **cond):
    """Iterate over mappings containing all pairs in cond."""
    items = cond.items()
    match = lambda m: all(k in m and m[k] == v for k, v in items)
    return filter(match, mappings)


def pluck(key, mappings):
    """Iterate over values for key in mappings."""
    return _map(itemgetter(key), mappings)


def pluckattr(attr, objects):
    """Iterate over values of given attribute of given objects."""
    return _map(attrgetter(attr), objects)



def invoke(objects, name, *args, **kwargs):
    """Yield results of the obj.name(*args, **kwargs) for each object in objects."""
    return _map(methodcaller(name, *args, **kwargs), objects)


def replace(iterable, pred, sub, window: int = 1, if_notfound: Literal["append", "forbid", "ignore"] = "append"):
    """Replace and optionally append if not found.

    Return seekable iterable.
    """
    sub = (sub,) if not isinstance(sub, tuple) else sub

    copy, iterable = spy(iterable)
    window_size = (window,) if window > -1 else ()
    found = ilen(locate(*(copy, pred, *window_size), consume=False)) > 0

    if found:
        return spy(list(mreplace(copy, pred, sub, *window_size)))[0]

    if if_notfound == "append":
        return spy(list(chain(copy, sub)))[0]
    if if_notfound == "forbid":
        raise ValueError("Replacement pattern not found")
    # "ignore"
    return spy(list(copy))[0]


### Generic ops
FACTORY_REPLACE = {
    type(object.__dict__): dict,
    type({}.keys()): list,
    type({}.values()): list,
    type({}.items()): list,
}


def _factory(coll: Iterable[_T] | Iterator[_T], mapper: Type[Dict] | None = None):
    coll_type = type(coll)
    # Hack for defaultdicts overridden constructor
    if isinstance(coll, defaultdict):
        item_factory = (
            compose(mapper, coll.default_factory) if mapper and coll.default_factory else coll.default_factory
        )
        return partial(defaultdict, cast(Callable, item_factory))
    if isinstance(coll, Iterator):
        return iter
    if isinstance(coll, bytes | str):
        return coll_type().join
    if coll_type in FACTORY_REPLACE:
        return FACTORY_REPLACE[coll_type]

    return cast(Callable[..., Iterable | Iterator], coll_type)


def empty(coll: Iterable[_T] | Iterator[_T]):
    """Creates an empty collection of the same type."""
    if isinstance(coll, SupportsIter):
        return iter([])
    return _factory(coll)()


def iterkeys(coll: "SupportsKeysItems"):
    return coll.keys() if hasattr(coll, "keys") else coll


def iteritems(coll: "SupportsKeysItems"):
    return coll.items() if hasattr(coll, "items") else coll


def itervalues(coll: "SupportsKeysItems"):
    return coll.values() if hasattr(coll, "values") else coll


iteritems.__doc__ = "Yields (key, value) pairs of the given collection."
itervalues.__doc__ = "Yields values of the given collection."
iterkeys.__doc__ = "Yields keys of the given collection."


def join(colls):
    """Join several collections of same type into one."""
    colls, colls_copy = tee(colls)
    it = iter(colls_copy)
    try:
        dest = next(it)
    except StopIteration:
        return None
    cls = dest.__class__

    if isinstance(dest, bytes | str):
        return "".join(colls)
    if isinstance(dest, Dict):
        result = dest.copy()
        for d in it:
            result.update(d)
        return result
    if isinstance(dest, set):
        return dest.union(*it)
    if isinstance(dest, Iterator | range):
        return chain.from_iterable(colls)
    if isinstance(dest, Iterable):
        # NOTE: this could be reduce(concat, ...),
        #       more effective for low count
        return cls(chain.from_iterable(colls))
    raise TypeError(f"Don't know how to join {cls.__name__}")


def merge(*colls):
    """Merge several collections of same type into one.

    Works with dicts, sets, lists, tuples, iterators and strings.
    For dicts later values take precedence.
    """
    return join(colls)


def join_with(f: Callable, dicts, strict=False):
    """Join several dicts, combining values with given function."""
    dicts = list(dicts)
    if not dicts:
        return {}
    if not strict and len(dicts) == 1:
        return dicts[0]

    lists = {}
    for c in dicts:
        for k, v in iteritems(c):
            if k in lists:
                lists[k].append(v)
            else:
                lists[k] = [v]

    if f is not list:
        # kind of walk_values() inplace
        for k, v in iteritems(lists):
            lists[k] = f(v)

    return lists


def merge_with(f: Callable, *dicts):
    """Merge several dicts, combining values with given function."""
    return join_with(f, dicts)


def walk(f: Callable[P, T], coll: Iterable[P]) -> Iterable[T]:
    """Walk the collection transforming its elements with f.

    Same as map, but preserves coll type.
    """
    return _factory(coll)(xmap(f, iteritems(coll)))


def walk_keys(f, coll):
    """Walk keys of the collection, mapping them with f."""
    f = make_func(f)

    # NOTE: we use this awkward construct instead of lambda to be Python 3 compatible
    def pair_f(pair):
        k, v = pair
        return f(k), v

    return walk(pair_f, coll)


def walk_values(f, coll):
    """Walk values of the collection, mapping them with f."""
    f = make_func(f)

    # NOTE: we use this awkward construct instead of lambda to be Python 3 compatible
    def pair_f(pair):
        k, v = pair
        return k, f(v)

    return _factory(coll, mapper=f)(xmap(pair_f, iteritems(coll)))


def prewalk(f, coll):
    """Walks the collection transforming its elements with f.

    Same as map, but preserves coll type.
    """
    return _factory(coll)(xmap(f, coll))


def select(pred, coll):
    """Same as filter but preserves coll type."""
    return _factory(coll)(filter(pred, iteritems(coll)))


def select_keys(pred, coll):
    """Select part of the collection with keys passing pred."""
    pred = make_pred(pred)
    return select(lambda pair: pred(pair[0]), coll)


def select_values(pred, coll):
    """Select part of the collection with values passing pred."""
    pred = make_pred(pred)
    return select(lambda pair: pred(pair[1]), coll)


def clean(coll):
    """Remove falsy values from the collection."""
    if isinstance(coll, Mapping):
        return select_values(bool, coll)
    return select(bool, coll)


# ### Content tests
_all = all
_any = any
xmap = map



# # TODO: a variant of some that returns mapped value,
# #       one can use some(map(f, seq)) or first(keep(f, seq)) for now.

# # TODO: vector comparison tests - ascending, descending and such
# # def chain_test(compare, seq):
# #     return all(compare, zip(seq, rest(seq))


def zipdict(keys, vals):
    """Create a dict with keys mapped to the corresponding vals."""
    return dict(zip(keys, vals, strict=False))


def flip(mapping):
    """Flip passed dict or collection of pairs swapping its keys and values."""

    def flip_pair(pair):
        k, v = pair
        return v, k

    return walk(flip_pair, mapping)


def project(mapping, keys):
    """Leave only given keys in mapping."""
    return _factory(mapping)((k, mapping[k]) for k in keys if k in mapping)


def omit(mapping, keys):
    """Remove given keys from mapping."""
    return _factory(mapping)((k, v) for k, v in iteritems(mapping) if k not in keys)



class collect(CollectIterator):
    

    def where(self, **cond):
        return type(self)(where(self, **cond))

    def pluck(self, key):
        return type(self)(pluck(key, self))
    
    def pluckattr(self,key):
        return type(self)(pluckattr(key, self))

    def haspath(self, path):
        return type(self)(haspath(self, path))

    def delin(self, path):
        return type(self)(delin(self, path))

    def getin(self, path, default=None):
        return type(self)(getin(self, path, default))

    def updatein(self, path, update, default=None):
        return type(self)(updatein(self, path, update, default))

    def setdefault(self, key, default=None, delimeter="."):
        return type(self)(setdefault(self, key, default, delimeter))

    def getlax(self, path, default=None):
        return type(self)(getlax(self, path, default))

    def walk(self, f):
        return type(self)(walk(f, self))

    def walk_keys(self, f):
        return type(self)(walk_keys(f, self))

    def walk_values(self, f):
        return type(self)(walk_values(f, self))

    def select(self, pred):
        return type(self)(select(pred, self))

    def select_keys(self, pred):
        return type(self)(select_keys(pred, self))

    def select_values(self, pred):
        return type(self)(select_values(pred, self))

    def clean(self):
        return type(self)(clean(self))

    def zipvalues(self, *others):
        return type(self)(zipvalues(self, *others))

    def zipdicts(self, *others):
        return type(self)(zipdicts(self, *others))

    def flip(self):
        return type(self)(flip(self))

    def project(self, keys):
        return type(self)(project(self, keys))

    def omit(self, keys):
        return type(self)(omit(self, keys))

    def zipdict(self, keys):
        return type(self)(zipdict(keys, self))

    def some(self, pred):
        return type(self)(some(pred, self))

    def all(self, pred):
        return type(self)(all(pred, self))

    def any(self, pred):
        return type(self)(any(pred, self))

    def none(self, pred):
        return type(self)(none(pred, self))

    def one(self, pred):
        return type(self)(one(pred, self))

    def isdistinct(self, key=EMPTY):
        return type(self)(isdistinct(self, key))

    def ilen(self):
        return ilen(self)

    def spy(self, length=None):
        return type(self)(spy(self, length))

    def locate(self, pred, window=None):
        return type(self)(locate(self, pred, window))

    def replace(self, pred, sub, window=1, if_notfound: Literal["append", "forbid", "ignore"] = "append"):
        return type(self)(replace(self, pred, sub, window, if_notfound))

    def join(self):
        return type(self)(join(self))

    def merge(self):
        return type(self)(merge(self))

    def join_with(self, f, strict=False):
        return type(self)(join_with(f, self, strict))

    def merge_with(self, f):
        return type(self)(merge_with(f, self))

    def flatten(self):
        return type(self)(flatten(self))

    def take(self, n):
        return type(self)(take(n, self))

    def drop(self, n):
        return type(self)(drop(n, self))

    def first(self, default=None):
        return type(self)(first(self, default))

    def last(self):
        return type(self)(last(self))

    def butlast(self):
        return type(self)(butlast(self))

    def rest(self):
        return type(self)(rest(self))

    def distinct(self):
        return type(self)(distinct(self))

    def map(self, f):
        return type(self)(_map(f, self))

    def filter(self, pred):
        return type(self)(filter(pred, self))

    def keep(self, pred):
        return type(self)(keep(pred, self))

    def remove(self, pred):
        return type(self)(remove(pred, self))

    def mapcat(self, f):
        return type(self)(mapcat(f, self))




    @wraps(collapse)
    def collapse(self, base_type: Type | None = None, levels=None):
        return type(self)(collapse(self, base_type, levels=levels))



def seekable(iterable: Iterable[_T]) -> Iterable[_T]:
    iterable = mseekable(iterable)
    iterable.seek(0)
    return iterable


def exists(key: str) -> Callable[[str], bool]:
    return lambda e: e is not None and key in e


# # # Type aliases
# # MethodAttr = Callable[[str, Sequence, Dict[str, Any]], Any]
# # MethodAttrCache = Dict[Callable, MethodAttr]


# # def arggetter(func: Callable, _cache: MethodAttrCache | None = None) -> MethodAttr:
# #     if _cache is None:
# #         _cache = {}
# #     if func in _cache:
# #         return _cache[func]

# #     original = getattr(func, "__original__", None) or unwrap(func)
# #     code: CodeType = original.__code__

# #     # Instrospect pos and kw names
# #     posnames = code.co_varnames[: code.co_argcount]
# #     n = code.co_argcount
# #     kwnames = code.co_varnames[n : n + code.co_kwonlyargcount]
# #     n += code.co_kwonlyargcount

# #     varposname = varkwname = None
# #     if code.co_flags & CO_VARARGS:
# #         varposname = code.co_varnames[n]
# #         n += 1
# #     if code.co_flags & CO_VARKEYWORDS:
# #         varkwname = code.co_varnames[n]

# #     allnames = set(code.co_varnames)
# #     indexes = {name: i for i, name in enumerate(posnames)}
# #     defaults = {}
# #     if original.__defaults__:
# #         defaults.update(zip(posnames[-len(original.__defaults__) :], original.__defaults__, strict=False))
# #     if original.__kwdefaults__:
# #         defaults.update(original.__kwdefaults__)

# #     def get_arg(name, args, kwargs):
# #         if name not in allnames:
# #             raise TypeError(f"{func.__name__}() doesn't have argument named {name}")

# #         index = indexes.get(name)
# #         if index is not None and index < len(args):
# #             return args[index]
# #         if name in kwargs and name in kwnames:
# #             return kwargs[name]
# #         if name == varposname:
# #             return args[len(posnames) :]
# #         if name == varkwname:
# #             return omit(kwargs, kwnames)
# #         if name in defaults:
# #             return defaults[name]
# #         raise TypeError(f"{func.__name__}() missing required argument: '{name}'")

# #     _cache[func] = get_arg
# #     return get_arg




# # _CallableT = TypeVar("_CallableT", bound=Callable[..., Any])
# # PWrapped = ParamSpec("PWrapped")
# # _argT = TypeVar("_argT")


# # class Call(Generic[_argT, _CallableT, PWrapped]):
# #     """Call object is just a proxy for decorated function with call arguments saved in its attributes.

# #     It serves as a way to partially apply arguments to a function and delay its execution,
# #     while maintaining access to the original function's attributes.

# #     Example:
# #         def log_api_call(call):
# #             print(f"Calling API endpoint: {call._args[0]}")
# #             return call()

# #         @decorator(log_api_call)
# #         def fetch_user(endpoint: str, user_id: int) -> dict:
# #             # Simulates API call
# #             return {"id": user_id, "endpoint": endpoint}

# #         # Creates a Call object with pre-filled arguments
# #         user_fetch = Call(fetch_user, "/users", user_id=123)

# #         # Later execution will log: "Calling API endpoint: /users"
# #         # And return: {"id": 123, "endpoint": "/users"}
# #         result = user_fetch()

# #     Args:
# #         func (Callable): The function to be wrapped
# #         *args: Positional arguments to be stored for later execution
# #         **kwargs: Keyword arguments to be stored for later execution

# #     Returns:
# #         Call: A Call instance that proxies the original function

# #     """

# #     def __init__(
# #         self,
# #         func: Callable[Concatenate[_argT, _PWrapped], _CallableT],
# #         *args: _PWrapped.args,
# #         **kwargs: _PWrapped.kwargs,
# #     ):
# #         self._func = func
# #         self._arg, *self._args = args
# #         self._kwargs = kwargs

# #     def __call__(self, *a: PWrapped.args, **kw: PWrapped.kwargs) -> _CallableT:  # Changed return type
# #         if not a and not kw:
# #             return self._func(self._arg, *self._args, **self._kwargs)

# #         return self._func(self._arg, *a, *self._args, **dict(self._kwargs, **kw))

# #     def __getattr__(self, name):
# #         try:
# #             res = self.__dict__[name] = arggetter(self._func)(name, self._args, self._kwargs)
# #             return res
# #         except TypeError as e:
# #             raise AttributeError(*e.args)

# #     def __str__(self):
# #         func = getattr(self._func, "__qualname__", str(self._func))
# #         args = ", ".join(list(map(str, self._args)) + ["%s=%s" % t for t in self._kwargs.items()])
# #         return "%s(%s)" % (func, args)

# #     def __repr__(self):
# #         return "<Call %s>" % self

# # def make_decorator(
# #     deco: Callable[[Call[R, Callable[P, R], P]], R],
# #     *dargs: P.args,
# #     **dkwargs: P.kwargs,
# # ) -> Callable[[Callable[P, R]], Callable[P, R]]:
# #     """Create a decorator that wraps functions using Call objects.

# #     Args:
# #         deco: A function that takes a Call object and returns R
# #         *dargs: Additional positional arguments for the decorator
# #         **dkwargs: Additional keyword arguments for the decorator

# #     Returns:
# #         A decorator function that maintains the original function's type signature

# #     """
# #     if dkwargs is None:
# #         dkwargs = {}

# #     @wraps(deco)
# #     def _decorator(func):
# #         def wrapper(*args, **kwargs):
# #             call = Call(func, args, kwargs)
# #             return deco(call, *dargs, **dkwargs)

# #         return wraps(func)(wrapper)

# #     # NOTE: should I update name to show args?
# #     # Save these for introspection
# #     # Preserve decorator metadata
# #     _decorator._func, _decorator._args, _decorator._kwargs = deco, dargs, dkwargs
# #     return wraps(deco)(_decorator)




# # __all__ = ["tree_leaves", "ltree_leaves", "tree_nodes"]




# # def rpartial(func, *args, **kwargs):
# #     """Partially applies last arguments.

# #     New keyworded arguments extend and override kwargs.
# #     """
# #     return lambda *a, **kw: func(*(a + args), **dict(kwargs, **kw))


# # def curry(func, n=EMPTY):
# #     """Curries func into a chain of one argument functions."""
# #     if n is EMPTY:
# #         n = get_spec(func).info.max_n

# #     if n <= 1:
# #         return func
# #     if n == 2:
# #         return lambda x: lambda y: func(x, y)
# #     return lambda x: curry(partial(func, x), n - 1)


# # def rcurry(func, n=EMPTY):
# #     """Curries func into a chain of one argument functions.

# #     Arguments are passed from right to left.
# #     """
# #     if n is EMPTY:
# #         n = get_spec(func).max_n

# #     if n <= 1:
# #         return func
# #     if n == 2:
# #         return lambda x: lambda y: func(y, x)
# #     return lambda x: rcurry(rpartial(func, x), n - 1)


# # def autocurry(func, n=EMPTY, _spec=None, _args=(), _kwargs=None):
# #     """Creates a version of func returning its partial applications
# #     until sufficient arguments are passed.
# #     """
# #     if _kwargs is None:
# #         _kwargs = {}
# #     spec = _spec or (get_spec(func) if n is EMPTY else Spec(n, set(), n, set(), False))

# #     @wraps(func)
# #     def autocurried(*a, **kw):
# #         args = _args + a
# #         kwargs = _kwargs.copy()
# #         kwargs.update(kw)

# #         if (
# #             not spec.varkw
# #             and len(args) + len(kwargs) >= spec.max_n
# #             or len(args) + len(set(kwargs) & spec.names) >= spec.max_n
# #         ):
# #             return func(*args, **kwargs)
# #         if len(args) + len(set(kwargs) & spec.req_names) >= spec.req_n:
# #             try:
# #                 return func(*args, **kwargs)
# #             except TypeError:
# #                 return autocurry(func, _spec=spec, _args=args, _kwargs=kwargs)
# #         else:
# #             return autocurry(func, _spec=spec, _args=args, _kwargs=kwargs)

# #     return autocurried


# # def iffy(pred: "Predicate", action: Callable | Empty = EMPTY, default: Callable = identity):
# #     """Creates a conditional function that applies different transformations based on a predicate.

# #     This function is useful when you need to conditionally transform values in data processing
# #     pipelines, similar to a functional if-else statement.

# #     Parameters
# #     ----------
# #     pred : callable or any
# #         Predicate function or value to test against. If not callable, will be converted
# #         to a predicate using `make_pred`.
# #     action : callable, optional
# #         Function to apply when predicate is True. If not provided, the predicate becomes
# #         the action and a bool predicate is used.
# #     default : callable or any, optional
# #         Function to apply when predicate is False. If not callable, the value itself is returned.
# #         Default is identity function.

# #     Returns
# #     -------
# #     callable
# #         A function that takes a value and returns either action(value) or default(value)
# #         based on the predicate result.

# #     Examples
# #     --------
# #     >>> is_positive = iffy(lambda x: x > 0, lambda x: 'positive', 'negative')
# #     >>> is_positive(5)
# #     'positive'
# #     >>> is_positive(-3)
# #     'negative'

# #     >>> remove_nulls = iffy(None, lambda _: None, lambda x: x)
# #     >>> remove_nulls(None)
# #     None
# #     >>> remove_nulls('hello')
# #     'hello'

# #     >>> double_evens = iffy(lambda x: x % 2 == 0, lambda x: x * 2)
# #     >>> double_evens(4)
# #     8
# #     >>> double_evens(3)
# #     3

# #     """
# #     """Creates a function, which conditionally applies action or default."""
# #     if action is EMPTY:
# #         return iffy(bool, pred, default)
# #     pred = make_pred(pred)
# #     action = make_func(action)
# #     return lambda v: action(v) if pred(v) else default(v) if callable(default) else default


class MissingT:
    pass


_initial_missing = MissingT()


def reduce(
    function: Callable[[_T | Callable[..., _T], _T], _T],
    sequence: Iterable[Callable[..., _T]] | _T,
    initial: Any | MissingT = _initial_missing,
) -> _T:
    """`reduce(function, iterable[, initial]) -> value`.

    Apply a function of two arguments cumulatively to the items of a sequence
    or iterable, from left to right, so as to reduce the iterable to a single
    value.  For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
    ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
    of the iterable in the calculation, and serves as a default when the
    iterable is empty.
    """
    it = iter(sequence)

    if initial is _initial_missing:
        try:
            value = next(it)
        except StopIteration:
            raise TypeError(
                "reduce() of empty iterable with no initial value",
            ) from None
    elif isinstance(initial, MissingT):
        raise TypeError("reduce() of empty sequence with no initial value")
    else:
        value = initial

    for element in it:
        value = function(value, element)

    return value




# # CallableT = TypeVar("CallableT", bound=Callable)


# # def decorator(deco: Callable[P, T]) -> Callable[[Callable[P, T]], Callable[P, T]]:
# #     """Transform a flat wrapper into decorator.

# #     Example:
# #         @decorator
# #         def func(call, methods, content_type=DEFAULT):  # These are decorator params
# #             # Access call arg by name
# #             if call.request.method not in methods:
# #                 # ...
# #             # Decorated functions and all the arguments are accesible as:
# #             print(call._func, call_args, call._kwargs)
# #             # Finally make a call:
# #             return call()

# #     """
# #     if has_single_arg(deco):
# #         return make_decorator(deco)
# #     if has_1pos_and_kwonly(deco):
# #         # Any arguments after first become decorator arguments
# #         # And a decorator with arguments is essentially a decorator fab
# #         def decorator_fab(_func=None, *dargs, **dkwargs):  # type: ignore
# #             if _func is not None:
# #                 return make_decorator(deco, *dargs, **dkwargs)(_func)
# #             return make_decorator(deco, *dargs, **dkwargs)
# #     else:

# #         def decorator_fab(*dargs, **dkwargs):
# #             return make_decorator(deco, *dargs, **dkwargs)

# #     return wraps(deco)(decorator_fab)









# # def _lfilter(f, seq):
# #     return list(filter(f, seq))


# # def calling(callable_attr: str, *args, **kwargs):
# #     """Create a function calling a method of the object with given args and kwargs."""
# #     return lambda obj: getattr(obj, callable_attr)(*args, **kwargs)


# # def accessing(attr: str):
# #     """Create a function accessing an attribute of the object."""
# #     return lambda obj: getattr(obj, attr)


# # async def asyncaccessing(attr: str):
# #     """Create a function accessing an attribute of the object."""

# #     async def _accessing(obj):
# #         return await getattr(obj, attr)

# #     return _accessing


# # accesses = accessing


# # def repeatedly(f, n=EMPTY):
# #     """Return Iterator that yields the result of f() endlessly or up to n times.

# #     Takes a function of no args, presumably with side effects,
# #     and returns an infinite (or length n) iterator of calls to it.
# #     """
# #     _repeat = repeat(None) if n is EMPTY else repeat(None, n)
# #     return (f() for _ in _repeat)


# # # @decorator
# # # def logcalls(call, print_func, errors=True, stack=True, repr_len=REPR_LEN):
# # #     """Log or print all function calls.

# # #     Includes call signature, arguments and return value, and errors.
# # #     """
# # #     signature = signature_repr(call, repr_len)
# # #     try:
# # #         print_func(f"Call {signature}")
# # #         result = call()
# # #         # NOTE: using full repr of result
# # #         print_func(f"-> {smart_repr(result, max_len=None)} from {signature}")
# # #         return result
# # #     except BaseException as e:
# # #         if errors:
# # #             print_func("-> " + _format_error(signature, e, stack))
# # #         raise


# # # def printcalls(errors=True, stack=True, repr_len=REPR_LEN):
# # #     if callable(errors):
# # #         return logcalls(print_func=print)(errors)

# # #     return logcalls(print, errors, stack, repr_len)


# # # printcalls.__doc__ = logcalls.__doc__


# # # @decorator
# # # def logenters(call, print_func, repr_len=REPR_LEN):
# # #     """Log each entrance to a function."""
# # #     print_func(f"Call {signature_repr(call, repr_len)}")
# # #     return call()


# # # def print_enters(repr_len=REPR_LEN):
# # #     """Print on each entrance to a function."""
# # #     if callable(repr_len):
# # #         return logenters(print)(repr_len)

# # #     return logenters(print, repr_len)


# # # @decorator
# # # def log_exits(call, print_func, errors=True, stack=True, repr_len=REPR_LEN):
# # #     """Log exits from a function."""
# # #     signature = signature_repr(call, repr_len)
# # #     try:
# # #         result = call()
# # #         # NOTE: using full repr of result
# # #         print_func(f"-> {smart_repr(result, max_len=None)} from {signature}")
# # #         return result
# # #     except BaseException as e:
# # #         if errors:
# # #             print_func("-> " + _format_error(signature, e, stack))
# # #         raise


# # # def print_exits(errors=True, stack=True, repr_len=REPR_LEN):
# # #     """Print on exits from a function."""
# # #     if callable(errors):
# # #         return log_exits(print)(errors)

# # #     return log_exits(print, errors, stack, repr_len)


# # class LabeledContextDecorator:
# #     """A context manager which also works as decorator, passing call signature as its label."""

# #     def __init__(self, print_func, label=None, repr_len=REPR_LEN):
# #         self.print_func = print_func
# #         self.label = label
# #         self.repr_len = repr_len

# #     def __call__(self, label=None, **kwargs):
# #         if callable(label):
# #             return self.decorator(label)

# #         return self.__class__(self.print_func, label, **kwargs)

# #     def decorator(self, func):
# #         @wraps(func)
# #         def inner(*args, **kwargs):
# #             # Recreate self with a new label so that nested and recursive calls will work
# #             cm = self.__class__.__new__(self.__class__)
# #             cm.__dict__.update(self.__dict__)
# #             cm.label = signature_repr(Call(func, args, kwargs), self.repr_len)
# #             with cm:
# #                 return func(*args, **kwargs)

# #         return inner


# # class log_errors(LabeledContextDecorator):  # noqa
# #     """Log or prints all errors within a function or block."""

# #     def __init__(self, print_func, label=None, stack=True, repr_len=REPR_LEN):
# #         LabeledContextDecorator.__init__(self, print_func, label=label, repr_len=repr_len)
# #         self.stack = stack

# #     def __enter__(self):
# #         return self

# #     def __exit__(self, exc_type, exc_value, tb):
# #         if exc_type:
# #             if self.stack:
# #                 exc_message = "".join(traceback.format_exception(exc_type, exc_value, tb))
# #             else:
# #                 exc_message = f"{exc_type.__name__}: {exc_value}"
# #             self.print_func(_format_error(self.label, exc_message, self.stack))


# # print_errors = log_errors(print)


# # # Duration utils


# # def format_time(sec):
# #     if sec < 1e-6:
# #         return "%8.2f ns" % (sec * 1e9)
# #     if sec < 1e-3:
# #         return "%8.2f mks" % (sec * 1e6)
# #     if sec < 1:
# #         return "%8.2f ms" % (sec * 1e3)

# #     return f"{sec:8.2f} s"


# # time_formatters = {
# #     "auto": format_time,
# #     "ns": lambda sec: "%8.2f ns" % (sec * 1e9),
# #     "mks": lambda sec: "%8.2f mks" % (sec * 1e6),
# #     "ms": lambda sec: "%8.2f ms" % (sec * 1e3),
# #     "s": lambda sec: f"{sec:8.2f} s",
# # }


# # class log_durations(LabeledContextDecorator):  # noqa
# #     """Times each function call or block execution."""

# #     def __init__(self, print_func, label=None, unit="auto", threshold=-1, repr_len=REPR_LEN):
# #         LabeledContextDecorator.__init__(self, print_func, label=label, repr_len=repr_len)
# #         if unit not in time_formatters:
# #             raise ValueError(f"Unknown time unit: {unit}. It should be ns, mks, ms, s or auto.")
# #         self.format_time = time_formatters[unit]
# #         self.threshold = threshold

# #     def __enter__(self):
# #         self.start = timer()
# #         return self

# #     def __exit__(self, *exc):
# #         duration = timer() - self.start
# #         if duration >= self.threshold:
# #             duration_str = self.format_time(duration)
# #             self.print_func(f"{duration_str} in {self.label}" if self.label else duration_str)


# # print_durations = log_durations(print)


# # def log_iter_durations(seq, print_func, label=None, unit="auto"):
# #     """Time processing of each item in seq."""
# #     if unit not in time_formatters:
# #         raise ValueError(f"Unknown time unit: {unit}. It should be ns, mks, ms, s or auto.")
# #     _format_time = time_formatters[unit]
# #     suffix = f" of {label}" if label else ""
# #     it = iter(seq)
# #     for i, item in enumerate(it):
# #         start = timer()
# #         yield item
# #         duration = _format_time(timer() - start)
# #         print_func("%s in iteration %d%s" % (duration, i, suffix))


# # def print_iter_durations(seq, label=None, unit="auto"):
# #     """Time processing of each item in seq."""
# #     return log_iter_durations(seq, print, label, unit=unit)


# # ### Formatting utils


# # def _format_error(label, e, stack=True):
# #     e_message = str(
# #         traceback.format_exc() if stack else f"{e.__class__.__name__}: {e}" if isinstance(e, Exception) else e,
# #     )

# #     if label:
# #         template = "%s    raised in %s" if stack else "%s raised in %s"
# #         return template % (e_message, label)

# #     return e_message


# # ### Call signature stringification utils


# # def signature_repr(call, repr_len=REPR_LEN):
# #     if isinstance(call._func, partial):
# #         name = f"<{call._func.func.__name__} partial>" if hasattr(call._func.func, "__name__") else "<unknown partial>"
# #     else:
# #         name = getattr(call._func, "__name__", "<unknown>")
# #     args_repr = (smart_repr(arg, repr_len) for arg in call._args)
# #     kwargs_repr = (f"{key}={smart_repr(value, repr_len)}" for key, value in call._kwargs.items())
# #     return "{}({})".format(name, ", ".join(chain(args_repr, kwargs_repr)))


# # def smart_repr(value, max_len: int | None = REPR_LEN):
# #     res = repr(value) if isinstance(value, bytes | str) else str(value)

# #     res = re.sub(r"\s+", " ", res)
# #     if max_len and len(res) > max_len:
# #         res = res[: max_len - 3] + "..."
# #     return res


# # class LazyObject:
# #     """A simplistic lazy init object.

# #     Rewrites itself when any attribute is accessed.
# #     """

# #     # NOTE: we can add lots of magic methods here to intercept on more events,
# #     #       this is postponed. As well as metaclass to support isinstance() check.
# #     def __init__(self, init):
# #         self.__dict__["_init"] = init

# #     def _setup(self):
# #         obj = self._init()
# #         object.__setattr__(self, "__class__", obj.__class__)
# #         object.__setattr__(self, "__dict__", obj.__dict__)

# #     def __getattr__(self, name):
# #         self._setup()
# #         return getattr(self, name)

# #     def __setattr__(self, name, value):
# #         self._setup()
# #         return setattr(self, name, value)


# # ### Initialization helpers
# # import threading


# # def once_per(*argnames):
# #     """Call function only once for every combination of the given arguments."""

# #     def once(func):
# #         lock = threading.Lock()
# #         done_set = set()
# #         done_list = []

# #         get_arg = arggetter(func)

# #         @wraps(func)
# #         def wrapper(*args, **kwargs):
# #             with lock:
# #                 values = tuple(get_arg(name, args, kwargs) for name in argnames)
# #                 if isinstance(values, Hashable):
# #                     done, add = done_set, done_set.add
# #                 else:
# #                     done, add = done_list, done_list.append

# #                 if values not in done:
# #                     add(values)
# #                     return func(*args, **kwargs)
# #                 return None

# #         return wrapper

# #     return once


# # once = once_per()
# # once.__doc__ = "Let function execute once, noop all subsequent calls."


# # def once_per_args(func):
# #     """Call function once for every combination of values of its arguments."""
# #     return once_per(*get_argnames(func))(func)


# # @decorator
# # def wrap_with(call, ctx):
# #     """Turn context manager into a decorator."""
# #     with ctx:
# #         return call()


# # mods |= {
# #     "identity",
# #     "constantly",
# #     "caller",
# #     "partial",
# #     "rpartial",
# #     "func_partial",
# #     "curry",
# #     "rcurry",
# #     "autocurry",
# #     "iffy",
# #     "compose",
# #     "rcompose",
# #     "complement",
# #     "juxt",
# #     "ljuxt",
# # }


# # # This provides sufficient introspection for *curry() functions.
# # #
# # # We only really need a number of required positional arguments.
# # # If arguments can be specified by name (not true for many builtin functions),
# # # then we need to now their names to ignore anything else passed by name.
# # #
# # # Stars mean some positional argument which can't be passed by name.
# # # Functions not mentioned here get one star "spec".
# # ARGS = {}


# # ARGS["builtins"] = {
# #     "bool": "*",
# #     "complex": "real,imag",
# #     "enumerate": "iterable,start",
# #     "file": "file-**",
# #     "float": "x",
# #     "int": "x-*",
# #     "long": "x-*",
# #     "open": "file-**",
# #     "round": "number-*",
# #     "setattr": "***",
# #     "str": "object-*",
# #     "unicode": "string-**",
# #     "__import__": "name-****",
# #     "__buildclass__": "***",
# #     # Complex functions with different set of arguments
# #     "iter": "*-*",
# #     "format": "*-*",
# #     "type": "*-**",
# # }
# # # Add two argument functions
# # two_arg_funcs = """cmp coerce delattr divmod filter getattr hasattr isinstance issubclass
# #                    map pow reduce"""
# # ARGS["builtins"].update(dict.fromkeys(two_arg_funcs.split(), "**"))


# # ARGS["functools"] = {"reduce": "**"}


# # ARGS["itertools"] = {
# #     "accumulate": "iterable-*",
# #     "combinations": "iterable,r",
# #     "combinations_with_replacement": "iterable,r",
# #     "compress": "data,selectors",
# #     "groupby": "iterable-*",
# #     "permutations": "iterable-*",
# #     "repeat": "object-*",
# # }
# # two_arg_funcs = "dropwhile filterfalse ifilter ifilterfalse starmap takewhile"
# # ARGS["itertools"].update(dict.fromkeys(two_arg_funcs.split(), "**"))


# # ARGS["operator"] = {
# #     "delslice": "***",
# #     "getslice": "***",
# #     "setitem": "***",
# #     "setslice": "****",
# # }
# # two_arg_funcs = """
# #     _compare_digest add and_ concat contains countOf delitem div eq floordiv ge getitem
# #     gt iadd iand iconcat idiv ifloordiv ilshift imatmul imod imul indexOf ior ipow irepeat
# #     irshift is_ is_not isub itruediv ixor le lshift lt matmul mod mul ne or_ pow repeat rshift
# #     sequenceIncludes sub truediv xor
# # """
# # ARGS["operator"].update(dict.fromkeys(two_arg_funcs.split(), "**"))
# # ARGS["operator"].update([("__{}__".format(op.strip("_")), args) for op, args in ARGS["operator"].items()])
# # ARGS["_operator"] = ARGS["operator"]


# # # Fixate this
# # STD_MODULES = set(ARGS)


# # # Describe some funcy functions, mostly for r?curry()
# # ARGS["funcy.seqs"] = {
# #     "map": "f*",
# #     "lmap": "f*",
# #     "xmap": "f*",
# #     "mapcat": "f*",
# #     "lmapcat": "f*",
# # }
# # ARGS["funcy.colls"] = {
# #     "merge_with": "f*",
# # }
# # _Ts = TypeVarTuple("_Ts")


# # class SpecInfo(NamedTuple, Generic[Unpack[_Ts],P,_T]):
# #     max_n: int
# #     names: Set[str]
# #     req_n: int
# #     req_names: Set[str]
# #     varkw: bool


# # U = TypeVar("U")

# # TupT = TypeVar("TupT", bound=Tuple)


# # SpecT = TypeVar("SpecT", bound=NamedTuple)


# # class Spec(NamedTuple):
# #     max_n: int
# #     names: Set[str]
# #     req_n: int
# #     req_names: Set[str]
# #     varkw: bool


# # def get_spec(func, _cache=None):
# #     if _cache is None:
# #         _cache = {}
# #     func = getattr(func, "__original__", None) or unwrap(func)
# #     try:
# #         return _cache[func]
# #     except (KeyError, TypeError):
# #         pass

# #     mod = getattr(func, "__module__", None)
# #     if mod in STD_MODULES or mod in ARGS and func.__name__ in ARGS[mod]:
# #         _spec = ARGS[mod].get(func.__name__, "*")
# #         required, _, optional = _spec.partition("-")
# #         req_names = re.findall(r"\w+|\*", required)  # a list with dups of *
# #         max_n = len(req_names) + len(optional)
# #         req_n = len(req_names)
# #         spec = SpecInfo(max_n=max_n, names=set(), req_n=req_n, req_names=set(req_names), varkw=False)
# #         _cache[func] = spec
# #         return spec
# #     if isinstance(func, type):
# #         # __init__ inherited from builtin classes
# #         objclass = getattr(func.__init__, "__objclass__", None)
# #         if objclass and objclass is not func:
# #             return get_spec(objclass)
# #         # Introspect constructor and remove self
# #         spec = get_spec(func.__init__)
# #         self_set = {func.__init__.__code__.co_varnames[0]}
# #         return spec._replace(
# #             max_n=spec.max_n - 1,
# #             names=spec.names - self_set,
# #             req_n=spec.req_n - 1,
# #             req_names=spec.req_names - self_set,
# #         )
# #     if hasattr(func, "__code__"):
# #         return _code_to_spec(func)
# #     # We use signature last to be fully backwards compatible. Also it's slower
# #     try:
# #         sig = signature(func)
# #         # import ipdb; ipdb.set_trace()
# #     except (ValueError, TypeError):
# #         raise ValueError(
# #             "Unable to introspect %s() arguments"
# #             % (getattr(func, "__qualname__", None) or getattr(func, "__name__", func)),
# #         )
# #     else:
# #         spec = _cache[func] = _sig_to_spec(sig)
# #         return spec


# # Ts = TypeVarTuple("Ts")


# # def _code_to_spec(func: Callable[[Callable[P, T]], Callable[P, T]]) -> SpecInfo[P, T]:
# #     code = func.__code__

# #     # Weird function like objects
# #     defaults = getattr(func, "__defaults__", None)
# #     defaults_n = len(defaults) if isinstance(defaults, tuple) else 0

# #     kwdefaults = getattr(func, "__kwdefaults__", None)
# #     if not isinstance(kwdefaults, dict):
# #         kwdefaults = {}

# #     posonly_n = getattr(code, "co_posonlyargcount", 0)

# #     varnames = code.co_varnames
# #     pos_n = code.co_argcount
# #     n = pos_n + code.co_kwonlyargcount
# #     names = set(varnames[posonly_n:n])
# #     req_n = n - defaults_n - len(kwdefaults)
# #     req_names = set(varnames[posonly_n : pos_n - defaults_n] + varnames[pos_n:n]) - set(kwdefaults)
# #     varkw = bool(code.co_flags & CO_VARKEYWORDS)
# #     # If there are varargs they could be required
# #     max_n = n + 1 if code.co_flags & CO_VARARGS else n
# #     return SpecInfo(max_n=max_n, names=names, req_n=req_n, req_names=req_names, varkw=varkw)


# # def _sig_to_spec(sig):
# #     max_n, names, req_n, req_names, varkw = 0, set(), 0, set(), False
# #     for name, param in sig.parameters.items():
# #         max_n += 1
# #         if param.kind == param.VAR_KEYWORD:
# #             max_n -= 1
# #             varkw = True
# #         elif param.kind == param.VAR_POSITIONAL:
# #             req_n += 1
# #         elif param.kind == param.POSITIONAL_ONLY:
# #             if param.default is param.empty:
# #                 req_n += 1
# #         else:
# #             names.add(name)
# #             if param.default is param.empty:
# #                 req_n += 1
# #                 req_names.add(name)
# #     return Spec(max_n=max_n, names=names, req_n=req_n, req_names=req_names, varkw=varkw)


# # mods |= {"memoize", "cache", "make_lookuper", "silent_lookuper", "EMPTY"}


# # class SkipMemory(Exception):
# #     pass


# # class Wrapper:
# #     invalidate: Callable
# #     invalidate_all: Callable
# #     memory: dict

# #     def __call__(self, *args: Any, **kwds: Any) -> Any:
# #         pass


# # def _memory_decorator(memory, key_func):
# #     def decorator(func):
# #         @wraps(func)
# #         def wrapper(*args, **kwargs):
# #             # We inline this here since @memoize also targets microoptimizations
# #             key = key_func(*args, **kwargs) if key_func else args + tuple(sorted(kwargs.items())) if kwargs else args
# #             try:
# #                 return memory[key]
# #             except KeyError:
# #                 try:
# #                     value = memory[key] = func(*args, **kwargs)
# #                     return value
# #                 except SkipMemory as e:
# #                     return e.args[0] if e.args else None

# #         def invalidate(*args, **kwargs):
# #             key = key_func(*args, **kwargs) if key_func else args + tuple(sorted(kwargs.items())) if kwargs else args
# #             memory.pop(key, None)

# #         wrapper.invalidate = invalidate

# #         def invalidate_all():
# #             memory.clear()

# #         wrapper.invalidate_all = invalidate_all

# #         wrapper.memory = memory
# #         return wrapper

# #     return decorator


# # class CacheMemory(dict):
# #     def __init__(self, timeout):
# #         self.timeout = timeout
# #         self.clear()

# #     def __setitem__(self, key, value):
# #         expires_at = time() + self.timeout
# #         dict.__setitem__(self, key, (value, expires_at))
# #         self._keys.append(key)
# #         self._expires.append(expires_at)

# #     def __getitem__(self, key):
# #         value, expires_at = dict.__getitem__(self, key)
# #         if expires_at <= time():
# #             self.expire()
# #             raise KeyError(key)
# #         return value

# #     def expire(self):
# #         i = bisect(self._expires, time())
# #         for _ in range(i):
# #             self._expires.popleft()
# #             self.pop(self._keys.popleft(), None)

# #     def clear(self):
# #         dict.clear(self)
# #         self._keys = deque()
# #         self._expires = deque()


# # class memoize:  # noqa: N801
# #     skip = SkipMemory

# #     def __call__(self, _func=None, /, *, key_func=None):
# #         """@memoize(key_func=None). Makes decorated function memoize its results.

# #         If key_func is specified uses key_func(*func_args, **func_kwargs) as memory key.
# #         Otherwise uses args + tuple(sorted(kwargs.items()))

# #         Exposes its memory via .memory attribute.
# #         """
# #         if _func is not None:
# #             return memoize()(_func)
# #         return _memory_decorator({}, key_func)

# #     def __new__(cls, *args, **kwargs):
# #         if args and callable(args[0]):
# #             return cls()(args[0])
# #         return super().__new__(cls)


# # class cache:  # noqa: N801
# #     skip = SkipMemory

# #     def __call__(self, timeout, *, key_func=None):
# #         """Caches a function results for timeout seconds."""
# #         if isinstance(timeout, timedelta):
# #             timeout = timeout.total_seconds()

# #         return _memory_decorator(CacheMemory(timeout), key_func)


# # def has_arg_types(func):
# #     params = signature(func).parameters.values()
# #     return any(p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD, p.VAR_POSITIONAL) for p in params), any(
# #         p.kind in (p.KEYWORD_ONLY, p.VAR_KEYWORD) for p in params
# #     )


# # def _make_lookuper(silent):
# #     def make_lookuper(func):
# #         """Create a single argument function looking up result in a memory.

# #         Decorated function is called once on first lookup and should return all available
# #         arg-value pairs.

# #         Resulting function will raise LookupError when using @make_lookuper
# #         or simply return None when using @silent_lookuper.
# #         """
# #         has_args, has_keys = has_arg_types(func)
# #         if has_keys:
# #             raise TypeError("Lookup table building function should not have keyword arguments")
# #         _wrapper: Callable
# #         if has_args:

# #             @memoize
# #             def args_wrapper(*args):
# #                 f = lambda: func(*args)
# #                 f.__name__ = "{}({})".format(func.__name__, ", ".join(map(str, args)))
# #                 return make_lookuper(f)

# #             _wrapper = args_wrapper
# #         else:
# #             memory = {}

# #             def arg_wrapper(arg):
# #                 if not memory:
# #                     memory[object()] = None  # prevent continuos memory refilling
# #                     memory.update(func())

# #                 if silent:
# #                     return memory.get(arg)
# #                 if arg in memory:
# #                     return memory[arg]
# #                 raise LookupError(f"Failed to look up {func.__name__}({arg})")

# #             _wrapper = arg_wrapper
# #         return wraps(func)(_wrapper)

# #     return make_lookuper


# # make_lookuper = _make_lookuper(False)
# # silent_lookuper = _make_lookuper(True)
# # silent_lookuper.__name__ = "silent_lookuper"


# # # # class PathLike(Path):
# # # #     from pathlib import PurePath
# # # #     from pathlib import ntpath
# # # #     from pathlib import posixpath
# # #     # parser = os.path
# # #     # if sys.version_info >= (3, 12): # noqa: UP036
# # #     #     _globber = os.fspath
# # #     # else:
# # #     #     _flavour = Path()._flavour # type: ignore # mypy bug
# # #     # __raw_path: str
# # #     # __raw_paths: list[str]

# # #     # def __add__(self, other:"str | Path | Traversable") -> Self:
# # #     #     """Simple string concatenation."""
# # #     #     return type(self)(str(self) + str(other))

# # #     # def __radd__(self, other:"str | Path | Traversable") -> Self:
# # #     #     """Simple string concatenation."""
# # #     #     return type(self)(str(other) + str(self))

# # #     # @property
# # #     # def _raw_path(self):
# # #     #     return self.__raw_path

# # #     # @_raw_path.setter
# # #     # def _raw_path(self, val):
# # #     #     self.__raw_path = val

# # #     # @property
# # #     # def _raw_paths(self):
# # #     #     return self.__raw_paths

# # #     # @_raw_paths.setter
# # #     # def _raw_paths(self, val):
# # #     #     self.__raw_paths = val

# # #     # @classmethod
# # #     # def cwd(cls) -> Self:
# # #     #     return super().cwd()

# # #     __div__ = Path.__truediv__
# # #     __rdiv__ = Path.__rtruediv__
# # #     __truediv__ = Path.__truediv__
# # #     __contains__ = compose(str,attrgetter("__contains__"))
# # #     startswith = compose(str,attrgetter("startswith"))
# # #     __str__ = Path.__str__
# # #     __iter__ = compose(str,attrgetter("__iter__"))
# # #     __enter__ = Path.__enter__
# # #     __eq__ = Path.__eq__
# # #     __ne__ = Path.__ne__

# # #     __slots__ = (
# # #         # The `_raw_paths` slot stores unnormalized string paths. This is set
# # #         # in the `__init__()` method.
# # #         '_raw_paths',

# # #         # The `_drv`, `_root` and `_tail_cached` slots store parsed and
# # #         # normalized parts of the path. They are set when any of the `drive`,
# # #         # `root` or `_tail` properties are accessed for the first time. The
# # #         # three-part division corresponds to the result of
# # #         # `os.path.splitroot()`, except that the tail is further split on path
# # #         # separators (i.e. it is a list of strings), and that the root and
# # #         # tail are normalized.
# # #         '_drv', '_root', '_tail_cached',

# # #         # The `_str` slot stores the string representation of the path,
# # #         # computed from the drive, root and tail when `__str__()` is called
# # #         # for the first time. It's used to implement `_str_normcase`
# # #         '_str',

# # #         # The `_str_normcase_cached` slot stores the string path with
# # #         # normalized case. It is set when the `_str_normcase` property is
# # #         # accessed for the first time. It's used to implement `__eq__()`
# # #         # `__hash__()`, and `_parts_normcase`
# # #         '_str_normcase_cached',

# # #         # The `_parts_normcase_cached` slot stores the case-normalized
# # #         # string path after splitting on path separators. It's set when the
# # #         # `_parts_normcase` property is accessed for the first time. It's used
# # #         # to implement comparison methods like `__lt__()`.
# # #         '_parts_normcase_cached',

# # #         # The `_lines_cached` slot stores the string path with path separators
# # #         # and newlines swapped. This is used to implement `match()`.
# # #         '_lines_cached',

# # #         # The `_hash` slot stores the hash of the case-normalized string
# # #         # path. It's set when `__hash__()` is called for the first time.
# # #         '_hash',
# # #     )

# # #     # def __init__(self,*args: "str | Path | Traversable") -> None:
# # #     #     self._flavor = type(self)._flavor
# # #     #     self._raw_path = "/".join(str(p) for p in args)
# # #     #     self._raw_paths = [str(p) for p in args]
# # #     _flavour = os.path

# # #     def __new__(cls, *args, **kwargs):
# # #         """Construct a PurePath from one or several strings and or existing
# # #         PurePath objects.  The strings and path objects are combined so as
# # #         to yield a canonicalized path, which is incorporated into the
# # #         new PurePath object.
# # #         """
# # #         if cls is PurePath:
# # #             cls = PureWindowsPath if os.name == 'nt' else PurePosixPath
# # #         return object.__new__(cls)

# # #     def __reduce__(self):
# # #         # Using the parts tuple helps share interned path parts
# # #         # when pickling related paths.
# # #         return (self.__class__, self.parts)

# # #     def __init__(self, *args):
# # #         paths = []
# # #         for arg in args:

# # #             if isinstance(arg, PurePath):
# # #                 if arg._flavour is ntpath and self._flavour is posixpath:
# # #                     # GH-103631: Convert separators for backwards compatibility.
# # #                     paths.extend(path.replace('\\', '/') for path in arg._raw_paths)
# # #                 else:
# # #                     paths.extend(arg._raw_paths)
# # #             else:
# # #                 try:
# # #                     path = os.fspath(arg)
# # #                 except TypeError:
# # #                     path = arg
# # #                 if not isinstance(path, str):
# # #                     raise TypeError(
# # #                         "argument should be a str or an os.PathLike "
# # #                         "object where __fspath__ returns a str, "
# # #                         f"not {type(path).__name__!r}")
# # #                 paths.append(path)
# # #         self._raw_paths = paths

# # #     def with_segments(self, *pathsegments):
# # #         """Construct a new path object from any number of path-like objects.
# # #         Subclasses may override this method to customize how new path objects
# # #         are created from methods like `iterdir()`.
# # #         """
# # #         return type(self)(*pathsegments)

# # #     @classmethod
# # #     def _parse_path(cls, path):
# # #         if not path:
# # #             return '', '', []
# # #         sep = cls._flavour.sep
# # #         altsep = cls._flavour.altsep
# # #         if altsep:
# # #             path = path.replace(altsep, sep)
# # #         drv, root, rel = cls._flavour.splitroot(path)
# # #         if not root and drv.startswith(sep) and not drv.endswith(sep):
# # #             drv_parts = drv.split(sep)
# # #             if len(drv_parts) == 4 and drv_parts[2] not in '?.':
# # #                 # e.g. //server/share
# # #                 root = sep
# # #             elif len(drv_parts) == 6:
# # #                 # e.g. //?/unc/server/share
# # #                 root = sep
# # #         parsed = [sys.intern(str(x)) for x in rel.split(sep) if x and x != '.']
# # #         return drv, root, parsed

# # #     def _load_parts(self):
# # #         paths = self._raw_paths
# # #         if len(paths) == 0:
# # #             path = ''
# # #         elif len(paths) == 1:
# # #             path = paths[0]
# # #         else:
# # #             path = self._flavour.join(*paths)
# # #         drv, root, tail = self._parse_path(path)
# # #         self._drv = drv
# # #         self._root = root
# # #         self._tail_cached = tail

# # #     def _from_parsed_parts(self, drv, root, tail):
# # #         path_str = self._format_parsed_parts(drv, root, tail)
# # #         path = self.with_segments(path_str)
# # #         path._str = path_str or '.'
# # #         path._drv = drv
# # #         path._root = root
# # #         path._tail_cached = tail
# # #         return path

# # #     @classmethod
# # #     def _format_parsed_parts(cls, drv, root, tail):
# # #         if drv or root:
# # #             return drv + root + cls._flavour.sep.join(tail)
# # #         elif tail and cls._flavour.splitdrive(tail[0])[0]:
# # #             tail = ['.'] + tail
# # #         return cls._flavour.sep.join(tail)

# # #     def __str__(self):
# # #         """Return the string representation of the path, suitable for
# # #         passing to system calls."""
# # #         try:
# # #             return self._str
# # #         except AttributeError:
# # #             self._str = self._format_parsed_parts(self.drive, self.root,
# # #                                                   self._tail) or '.'
# # #             return self._str

# # #     def __fspath__(self):
# # #         return str(self)

# # #     def as_posix(self):
# # #         """Return the string representation of the path with forward (/)
# # #         slashes."""
# # #         f = self._flavour
# # #         return str(self).replace(f.sep, '/')

# # #     def __bytes__(self):
# # #         """Return the bytes representation of the path.  This is only
# # #         recommended to use under Unix."""
# # #         return os.fsencode(self)

# # #     def __repr__(self):
# # #         return "{}({!r})".format(self.__class__.__name__, self.as_posix())

# # #     def as_uri(self):
# # #         """Return the path as a 'file' URI."""
# # #         if not self.is_absolute():
# # #             raise ValueError("relative path can't be expressed as a file URI")

# # #         drive = self.drive
# # #         if len(drive) == 2 and drive[1] == ':':
# # #             # It's a path on a local drive => 'file:///c:/a/b'
# # #             prefix = 'file:///' + drive
# # #             path = self.as_posix()[2:]
# # #         elif drive:
# # #             # It's a path on a network drive => 'file://host/share/a/b'
# # #             prefix = 'file:'
# # #             path = self.as_posix()
# # #         else:
# # #             # It's a posix path => 'file:///etc/hosts'
# # #             prefix = 'file://'
# # #             path = str(self)
# # #         return prefix + urlquote_from_bytes(os.fsencode(path))

# # #     @property
# # #     def _str_normcase(self):
# # #         # String with normalized case, for hashing and equality checks
# # #         try:
# # #             return self._str_normcase_cached
# # #         except AttributeError:
# # #             if _is_case_sensitive(self._flavour):
# # #                 self._str_normcase_cached = str(self)
# # #             else:
# # #                 self._str_normcase_cached = str(self).lower()
# # #             return self._str_normcase_cached

# # #     @property
# # #     def _parts_normcase(self):
# # #         # Cached parts with normalized case, for comparisons.
# # #         try:
# # #             return self._parts_normcase_cached
# # #         except AttributeError:
# # #             self._parts_normcase_cached = self._str_normcase.split(self._flavour.sep)
# # #             return self._parts_normcase_cached

# # #     @property
# # #     def _lines(self):
# # #         # Path with separators and newlines swapped, for pattern matching.
# # #         try:
# # #             return self._lines_cached
# # #         except AttributeError:
# # #             path_str = str(self)
# # #             if path_str == '.':
# # #                 self._lines_cached = ''
# # #             else:
# # #                 trans = _SWAP_SEP_AND_NEWLINE[self._flavour.sep]
# # #                 self._lines_cached = path_str.translate(trans)
# # #             return self._lines_cached

# # #     def __eq__(self, other):
# # #         if not isinstance(other, PurePath):
# # #             return NotImplemented
# # #         return self._str_normcase == other._str_normcase and self._flavour is other._flavour

# # #     def __hash__(self):
# # #         try:
# # #             return self._hash
# # #         except AttributeError:
# # #             self._hash = hash(self._str_normcase)
# # #             return self._hash

# # #     def __lt__(self, other):
# # #         if not isinstance(other, PurePath) or self._flavour is not other._flavour:
# # #             return NotImplemented
# # #         return self._parts_normcase < other._parts_normcase

# # #     def __le__(self, other):
# # #         if not isinstance(other, PurePath) or self._flavour is not other._flavour:
# # #             return NotImplemented
# # #         return self._parts_normcase <= other._parts_normcase

# # #     def __gt__(self, other):
# # #         if not isinstance(other, PurePath) or self._flavour is not other._flavour:
# # #             return NotImplemented
# # #         return self._parts_normcase > other._parts_normcase

# # #     def __ge__(self, other):
# # #         if not isinstance(other, PurePath) or self._flavour is not other._flavour:
# # #             return NotImplemented
# # #         return self._parts_normcase >= other._parts_normcase

# # #     @property
# # #     def drive(self):
# # #         """The drive prefix (letter or UNC path), if any."""
# # #         try:
# # #             return self._drv
# # #         except AttributeError:
# # #             self._load_parts()
# # #             return self._drv

# # #     @property
# # #     def root(self):
# # #         """The root of the path, if any."""
# # #         try:
# # #             return self._root
# # #         except AttributeError:
# # #             self._load_parts()
# # #             return self._root

# # #     @property
# # #     def _tail(self):
# # #         try:
# # #             return self._tail_cached
# # #         except AttributeError:
# # #             self._load_parts()
# # #             return self._tail_cached

# # #     @property
# # #     def anchor(self):
# # #         """The concatenation of the drive and root, or ''."""
# # #         anchor = self.drive + self.root
# # #         return anchor

# # #     @property
# # #     def name(self):
# # #         """The final path component, if any."""
# # #         tail = self._tail
# # #         if not tail:
# # #             return ''
# # #         return tail[-1]

# # #     @property
# # #     def suffix(self):
# # #         """
# # #         The final component's last suffix, if any.

# # #         This includes the leading period. For example: '.txt'
# # #         """
# # #         name = self.name
# # #         i = name.rfind('.')
# # #         if 0 < i < len(name) - 1:
# # #             return name[i:]
# # #         else:
# # #             return ''

# # #     @property
# # #     def suffixes(self):
# # #         """
# # #         A list of the final component's suffixes, if any.

# # #         These include the leading periods. For example: ['.tar', '.gz']
# # #         """
# # #         name = self.name
# # #         if name.endswith('.'):
# # #             return []
# # #         name = name.lstrip('.')
# # #         return ['.' + suffix for suffix in name.split('.')[1:]]

# # #     @property
# # #     def stem(self):
# # #         """The final path component, minus its last suffix."""
# # #         name = self.name
# # #         i = name.rfind('.')
# # #         if 0 < i < len(name) - 1:
# # #             return name[:i]
# # #         else:
# # #             return name

# # #     def with_name(self, name):
# # #         """Return a new path with the file name changed."""
# # #         if not self.name:
# # #             raise ValueError("%r has an empty name" % (self,))
# # #         f = self._flavour
# # #         if not name or f.sep in name or (f.altsep and f.altsep in name) or name == '.':
# # #             raise ValueError("Invalid name %r" % (name))
# # #         return self._from_parsed_parts(self.drive, self.root,
# # #                                        self._tail[:-1] + [name])

# # #     def with_stem(self, stem):
# # #         """Return a new path with the stem changed."""
# # #         return self.with_name(stem + self.suffix)

# # #     def with_suffix(self, suffix):
# # #         """Return a new path with the file suffix changed.  If the path
# # #         has no suffix, add given suffix.  If the given suffix is an empty
# # #         string, remove the suffix from the path.
# # #         """
# # #         f = self._flavour
# # #         if f.sep in suffix or f.altsep and f.altsep in suffix:
# # #             raise ValueError("Invalid suffix %r" % (suffix,))
# # #         if suffix and not suffix.startswith('.') or suffix == '.':
# # #             raise ValueError("Invalid suffix %r" % (suffix))
# # #         name = self.name
# # #         if not name:
# # #             raise ValueError("%r has an empty name" % (self,))
# # #         old_suffix = self.suffix
# # #         if not old_suffix:
# # #             name = name + suffix
# # #         else:
# # #             name = name[:-len(old_suffix)] + suffix
# # #         return self._from_parsed_parts(self.drive, self.root,
# # #                                        self._tail[:-1] + [name])

# # #     def relative_to(self, other, /, *_deprecated, walk_up=False):
# # #         """Return the relative path to another path identified by the passed
# # #         arguments.  If the operation is not possible (because this is not
# # #         related to the other path), raise ValueError.

# # #         The *walk_up* parameter controls whether `..` may be used to resolve
# # #         the path.
# # #         """
# # #         if _deprecated:
# # #             msg = ("support for supplying more than one positional argument "
# # #                    "to pathlib.PurePath.relative_to() is deprecated and "
# # #                    "scheduled for removal in Python {remove}")
# # #             warnings._deprecated("pathlib.PurePath.relative_to(*args)", msg,
# # #                                  remove=(3, 14))
# # #         other = self.with_segments(other, *_deprecated)
# # #         for step, path in enumerate([other] + list(other.parents)):
# # #             if self.is_relative_to(path):
# # #                 break
# # #             elif not walk_up:
# # #                 raise ValueError(f"{str(self)!r} is not in the subpath of {str(other)!r}")
# # #             elif path.name == '..':
# # #                 raise ValueError(f"'..' segment in {str(other)!r} cannot be walked")
# # #         else:
# # #             raise ValueError(f"{str(self)!r} and {str(other)!r} have different anchors")
# # #         parts = ['..'] * step + self._tail[len(path._tail):]
# # #         return self.with_segments(*parts)

# # #     def is_relative_to(self, other, /, *_deprecated):
# # #         """Return True if the path is relative to another path or False.
# # #         """
# # #         if _deprecated:
# # #             msg = ("support for supplying more than one argument to "
# # #                    "pathlib.PurePath.is_relative_to() is deprecated and "
# # #                    "scheduled for removal in Python {remove}")
# # #             warnings._deprecated("pathlib.PurePath.is_relative_to(*args)",
# # #                                  msg, remove=(3, 14))
# # #         other = self.with_segments(other, *_deprecated)
# # #         return other == self or other in self.parents

# # #     @property
# # #     def parts(self):
# # #         """An object providing sequence-like access to the
# # #         components in the filesystem path."""
# # #         if self.drive or self.root:
# # #             return (self.drive + self.root,) + tuple(self._tail)
# # #         else:
# # #             return tuple(self._tail)

# # #     def joinpath(self, *pathsegments):
# # #         """Combine this path with one or several arguments, and return a
# # #         new path representing either a subpath (if all arguments are relative
# # #         paths) or a totally different path (if one of the arguments is
# # #         anchored).
# # #         """
# # #         return self.with_segments(self, *pathsegments)

# # #     def __truediv__(self, key):
# # #         try:
# # #             return self.joinpath(key)
# # #         except TypeError:
# # #             return NotImplemented

# # #     def __rtruediv__(self, key):
# # #         try:
# # #             return self.with_segments(key, self)
# # #         except TypeError:
# # #             return NotImplemented

# # #     @property
# # #     def parent(self):
# # #         """The logical parent of the path."""
# # #         drv = self.drive
# # #         root = self.root
# # #         tail = self._tail
# # #         if not tail:
# # #             return self
# # #         return self._from_parsed_parts(drv, root, tail[:-1])

# # #     @property
# # #     def parents(self):
# # #         """A sequence of this path's logical parents."""
# # #         # The value of this property should not be cached on the path object,
# # #         # as doing so would introduce a reference cycle.
# # #         return _PathParents(self)

# # #     def is_absolute(self):
# # #         """True if the path is absolute (has both a root and, if applicable,
# # #         a drive)."""
# # #         if self._flavour is ntpath:
# # #             # ntpath.isabs() is defective - see GH-44626.
# # #             return bool(self.drive and self.root)
# # #         elif self._flavour is posixpath:
# # #             # Optimization: work with raw paths on POSIX.
# # #             for path in self._raw_paths:
# # #                 if path.startswith('/'):
# # #                     return True
# # #             return False
# # #         else:
# # #             return self._flavour.isabs(str(self))

# # #     def is_reserved(self):
# # #         """Return True if the path contains one of the special names reserved
# # #         by the system, if any."""
# # #         if self._flavour is posixpath or not self._tail:
# # #             return False

# # #         # NOTE: the rules for reserved names seem somewhat complicated
# # #         # (e.g. r"..\NUL" is reserved but not r"foo\NUL" if "foo" does not
# # #         # exist). We err on the side of caution and return True for paths
# # #         # which are not considered reserved by Windows.
# # #         if self.drive.startswith('\\\\'):
# # #             # UNC paths are never reserved.
# # #             return False
# # #         name = self._tail[-1].partition('.')[0].partition(':')[0].rstrip(' ')
# # #         return name.upper() in _WIN_RESERVED_NAMES

# # #     def match(self, path_pattern, *, case_sensitive=None):
# # #         """
# # #         Return True if this path matches the given pattern.
# # #         """
# # #         if not isinstance(path_pattern, PurePath):
# # #             path_pattern = self.with_segments(path_pattern)
# # #         if case_sensitive is None:
# # #             case_sensitive = _is_case_sensitive(self._flavour)
# # #         pattern = _compile_pattern_lines(path_pattern._lines, case_sensitive)
# # #         if path_pattern.drive or path_pattern.root:
# # #             return pattern.match(self._lines) is not None
# # #         elif path_pattern._tail:
# # #             return pattern.search(self._lines) is not None
# # #         else:
# # #             raise ValueError("empty pattern")

# # #     __init__ = Path.__init__

# # #     __call__ = Path.__call__

# # #     def __new__(cls, *paths: "str | Path | Traversable") -> Self:
# # #         return Path.__new__(Path, str(Path(*paths)))
# # #         # cls._flavour = "posix"
# # #         # cls.__raw_paths = []

# # #         # if isinstance(paths, list | tuple) and len(paths) > 1:
# # #         #     paths = tuple(str(p) for p in paths)
# # #         #     path = Path.__new__(cls, *paths)
# # #         #     path._raw_path = str(path)
# # #         #     path._raw_paths = cast(list[str],paths)
# # #         #     path.__raw_paths = cast(list[str],paths)
# # #         #     return path
# # #         # if len(paths) == 1:
# # #         #     raw_path = str(paths[0])
# # #         #     path = Path.__new__(cls, raw_path)
# # #         #     path._raw_path = raw_path
# # #         #     path._raw_paths = [str(p) for p in paths]
# # #         #     return path
# # #         # path = super().__new__(cls,_raw_path="",_raw_paths=[])
# # #         # path._raw_path = ""
# # #         # path._raw_paths = []
# # #         # path.__raw_paths = []
# # #         # return path

# # #     # def __contains__(self, item: "str | Path | Traversable") -> bool:
# # #     #     return str(item) in str(self)

# # #     # def __getitem__(self, key: int|slice) -> str:
# # #     #     return str(self).__getitem__(key)

# # #     # def startswith(self, *parts: "str | Path | Traversable") -> bool:
# # #     #     return str(self).startswith(str(PathLike(*parts)))

# # #     # def endswith(self, *parts: "str | Path | Traversable") -> bool:
# # #     #     return str(self).endswith(str(PathLike(*parts)))

# # #     # def split(self,delim=None) -> list[str]:
# # #     #     return str(self).split(delim)
# # #     # def splitparts(self) -> list[str]:
# # #     #     return str(self).split("/")


# # #     # def __truediv__(self, *args: "str | Path | Traversable") -> Self:
# # #     #     return Path.__truediv__(self, *args)
# # #     # def __div__(self, *args: "str | Path | Traversable") -> Self:
# # #     #     return Path.__div__(self, *args)

# # #     # def __rdiv__(self, *args: "str | Path | Traversable") -> Self:
# # #     #     return Path.__rdiv__(self, *args)

# # # PathType = Path | str | PathLike

# # PathLike = Path
# # PathType = Path | str | PathLike
