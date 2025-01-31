#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins


#--------------------------------------------------------------------------------
# 클래스 프로퍼티 데코레이터.
# - 사용시 해당 데코레이터의 대상 메서드는 클래스 메서드로 인지.
#--------------------------------------------------------------------------------
T = TypeVar("T")
def classproperty(targetMethod: Callable[[Type[T]], Any]) -> Any:
    class ClassPropertyDescriptor:
        def __init__(thisInstance, fget: Callable[[Type[T]], Any]) -> None:
            thisInstance.fget = fget
            thisInstance.fset: Optional[Callable[[Type[T], Any], None]] = None
            thisInstance.fdel: Optional[Callable[[Type[T]], None]] = None
        def __get__(thisInstance, obj: Optional[T], cls: Type[T]) -> Any:
            if thisInstance.fget is None:
                raise AttributeError("Unreadable attribute")
            return thisInstance.fget(cls)
        def __set__(thisInstance, obj: Optional[T], value: Any) -> None:
            if thisInstance.fset is None:
                raise AttributeError("Can't set attribute")
            if obj is None:
                cls = type(value)
            else:
                cls = type(obj)
            thisInstance.fset(cls, value)
        def __delete__(thisInstance, obj: Optional[T]) -> None:
            if thisInstance.fdel is None:
                raise AttributeError("Can't delete attribute")
            cls = type(obj)
            thisInstance.fdel(cls)
        def setter(thisInstance, fset: Callable[[Type[T], Any], None]) -> "ClassPropertyDescriptor":
            thisInstance.fset = fset
            return thisInstance
        def deleter(thisInstance, fdel: Callable[[Type[T]], None]) -> "ClassPropertyDescriptor":
            thisInstance.fdel = fdel
            return thisInstance
    return ClassPropertyDescriptor(targetMethod)