#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from threading import Lock
from ..core import BaseClass
# from ..decorator import classproperty


#--------------------------------------------------------------------------------
# 베이스 매니저 클래스.
#--------------------------------------------------------------------------------
T = TypeVar("T", bound = "BaseManager")
class BaseManager(BaseClass, Generic[T]):
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__SharedInstance: T = None
	__Lock: Lock = Lock()


	#--------------------------------------------------------------------------------
	# 공유 인스턴스 프로퍼티.
	#--------------------------------------------------------------------------------
	# @classproperty
	@classmethod
	@property
	def Instance(thisClassType: Type[T]) -> T:
		if thisClassType.__SharedInstance is None:
			with thisClassType.__Lock:
				if thisClassType.__SharedInstance is None:
					thisClassType.__SharedInstance = thisClassType()
		return thisClassType.__SharedInstance


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		# base = super()
		# base.__init__()
		pass