#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import os
from ..console import Console
from .entry import Entry


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY: str = ""



#--------------------------------------------------------------------------------
# 스토리지 항목.
#--------------------------------------------------------------------------------
T = TypeVar("T", bound = Entry)
class Storage(Entry[T]):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, name: str, **argumentDictionary) -> None:
		base = super()
		base.__init__(name, **argumentDictionary)

		# 마운트 된 스토리지 위에 또 다른 마운트 된 부모 스토리지가 존재할 수 있는가?
		# base.Parent = None