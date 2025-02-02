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
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"
UTF8: str = "utf-8"
EMPTY: str = ""
SPACE: str = " "


#--------------------------------------------------------------------------------
# XML 경로. (XPath 스펙 일부 구현)
#--------------------------------------------------------------------------------
class Path:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__value: str
	__namespaces: dict


	#--------------------------------------------------------------------------------
	# 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Value(thisInstance, value: str = "") -> str:
		return thisInstance.__value


	#--------------------------------------------------------------------------------
	# 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@Value.setter
	def Value(thisInstance, value: str) -> None:
		thisInstance.__value = value


	#--------------------------------------------------------------------------------
	# 네임스페이스 목록 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Namespaces(thisInstance) -> Dict[str, str]:
		return thisInstance.__namespaces


	#--------------------------------------------------------------------------------
	# 네임스페이스 목록 프로퍼티.
	#--------------------------------------------------------------------------------
	@Namespaces.setter
	def Namespaces(thisInstance, value: Dict[str, str]) -> None:
		thisInstance.__namespaces = value


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메소드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, value: str = "", namespaces: Optional[Dict[str, str]] = None) -> None:
		thisInstance.__value = value
		thisInstance.__namespaces = namespaces


	#--------------------------------------------------------------------------------
	# 문자열 변환.
	#--------------------------------------------------------------------------------
	def __str__(thisInstance) -> str:
		return thisInstance.__value