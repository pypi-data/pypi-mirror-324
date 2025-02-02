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
import functools
import inspect


#--------------------------------------------------------------------------------
# 오버라이드 메소드 데코레이터.
# - 아무 기능 없고 단순 표기용으로 이 메소드가 오버라이드 된 상태를 의미함.
# - 일반 함수는 사용할 수 없고 클래스 메소드, 인스턴스 메소드, 정적 메소드 사용 가능.
#--------------------------------------------------------------------------------
def overridemethod(targetMethod : Callable) -> Callable:
	@functools.wraps(targetMethod)
	def Wrapper(*argumentTuple : list[Any], **argumentDictionary : dict[str, Any]) -> None:		
		# 클래스 메소드, 인스턴스 메소드 확인.
		# 특별한 검사 필요 없음.
		if inspect.ismethod(targetMethod):
			return targetMethod(*argumentTuple, **argumentDictionary)
		# 정적 메소드 확인.
		elif isinstance(targetMethod, staticmethod):
			return targetMethod(*argumentTuple, **argumentDictionary)
		raise TypeError(f"'{targetMethod.__name__}'은(는) 클래스 메소드, 인스턴스 메소드 또는 정적 메소드에서만 사용할 수 있습니다.")
	return Wrapper