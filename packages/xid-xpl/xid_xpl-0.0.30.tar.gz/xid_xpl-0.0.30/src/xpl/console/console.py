#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Literal, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, AnyStr, List, Dict, Set
from typing import Protocol
from typing import cast, overload
import builtins


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
SPACE: str = " "
LINEFEED: str = "\n"


#--------------------------------------------------------------------------------
# 파이썬 내장 모듈만으로 SupportsWrite가 지원되지 않을 경우에 대한 처리.
# - 스트림 쓰기 함수가 존재할 경우 연동가능 용도.
#--------------------------------------------------------------------------------
T = TypeVar("T", covariant = True)
class SupportsWrite(Protocol[T]):
	#--------------------------------------------------------------------------------
	# 쓰기.
	#--------------------------------------------------------------------------------
    def write(thisInstance, data: str) -> None:
        ...


#--------------------------------------------------------------------------------
# 빌트인 확장 클래스. (Builtins ==> Python)
# - 파이썬의 기본 시스템 내장 함수들은 빌트인 모듈로 접근하여 사용 가능.
# - bultins.print(), print(), Console.Print는 동일한 함수.
#--------------------------------------------------------------------------------
class Console:
	"""파이썬 빌트인 클래스"""
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__IsPrintEnable: bool = True


	#--------------------------------------------------------------------------------
	# 출력 활성화. (기본적으로 활성화 되어있음.)
	#--------------------------------------------------------------------------------
	@classmethod
	def IsPrintEnable(thisClassType, isEnable: bool) -> None:
		"""출력 활성화 (기본값: True)"""
		Console.__IsPrintEnable = isEnable


	#--------------------------------------------------------------------------------
	# 출력.
	#--------------------------------------------------------------------------------
	@classmethod
	def Print(thisClassType, *values: object) -> None:
		"""문자열 출력. (간단한 버전)"""
		if not Console.__IsPrintEnable:
			return
		builtins.print(*values)


	#--------------------------------------------------------------------------------
	# 출력.
	#--------------------------------------------------------------------------------
	@classmethod
	def PrintDetailed(thisClassType, *values: object, sep: Optional[str] = SPACE, end: Optional[str] = LINEFEED, file: SupportsWrite[str] | None = None, flush: Literal[False] = False) -> None:
		"""문자열 출력. (상세한 버전)"""
		if not Console.__IsPrintEnable:
			return
		builtins.print(*values, sep = sep, end = end, file = file, flush = flush)