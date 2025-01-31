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
import weakref
from .baseclass import BaseClass


#--------------------------------------------------------------------------------
# 오브젝트의 약한 참조 개체.
#--------------------------------------------------------------------------------
T = TypeVar("T", bound = BaseClass)
class WeakedReference(BaseClass, Generic[T]):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__weakedReference: weakref.ReferenceType[T]


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, target: T) -> None:
		base = super()
		base.__init__()
		thisInstance.__weakedReference = weakref.ref(target)


	#--------------------------------------------------------------------------------
	# 호출 프로토콜 메서드.
	#--------------------------------------------------------------------------------
	def __call__(thisInstance) -> Optional[T]:
		return thisInstance.__weakedReference
	

	#--------------------------------------------------------------------------------
	# 멤버 반환 프로토콜 메서드.
	#--------------------------------------------------------------------------------
	def __getattr__(thisInstance, name: str) -> Any:
		try:
			target = thisInstance.__weakedReference()
			if not target:
				raise ReferenceError()
			return builtins.getattr(target, name)
		except Exception as exception:
			raise