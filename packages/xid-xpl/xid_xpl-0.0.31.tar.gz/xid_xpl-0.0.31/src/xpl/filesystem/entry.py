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
from ..core import BaseNode


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY: str = ""



#--------------------------------------------------------------------------------
# 파일 시스템의 단위 항목.
#--------------------------------------------------------------------------------
TEntry = TypeVar("TEntry", bound = "Entry")
class Entry(BaseNode[TEntry]):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__path: str


	#--------------------------------------------------------------------------------
	# 전체 이름.
	#--------------------------------------------------------------------------------
	@property
	def FullName(thisInstance) -> str:
		return f"{thisInstance.__path}{thisInstance.Name}{thisInstance.__extension}"
	

	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, name: str, **argumentDictionary) -> None:
		base = super()
		base.__init__(name, **argumentDictionary)

		thisInstance.__path = argumentDictionary.get("path")
		thisInstance.__extension = argumentDictionary.get("extension")
		thisInstance.__fileFullName = f"{thisInstance.__path}{thisInstance.Name}{thisInstance.__extension}"


	#--------------------------------------------------------------------------------
	# 실제 존재 여부.
	#--------------------------------------------------------------------------------
	def Exists(thisInstance) -> bool:
		isExists: bool = os.path.exists(thisInstance.__path)
		return isExists