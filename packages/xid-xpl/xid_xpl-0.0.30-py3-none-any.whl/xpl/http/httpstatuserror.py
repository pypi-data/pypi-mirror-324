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
# 상태코드 에러.
#--------------------------------------------------------------------------------
class HTTPStatusError(Exception):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__text: str
	__statusCode: int


	#--------------------------------------------------------------------------------
	# 오류메시지.
	#--------------------------------------------------------------------------------
	@property
	def Text(thisInstance) -> int:
		return thisInstance.__text
	

	#--------------------------------------------------------------------------------
	# 상태코드.
	#--------------------------------------------------------------------------------
	@property
	def StatusCode(thisInstance) -> int:
		return thisInstance.__statusCode
	

	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, statusCode: int, text: str = ""):
			thisInstance.__statusCode = statusCode
			thisInstance.__text = text
			base = super()
			if thisInstance.__text:
				base.__init__(f"HTTPStatusError: {thisInstance.__text} ({thisInstance.__statusCode})")
			else:
				base.__init__(f"HTTPStatusError: Status Code Exception. ({thisInstance.__statusCode})")