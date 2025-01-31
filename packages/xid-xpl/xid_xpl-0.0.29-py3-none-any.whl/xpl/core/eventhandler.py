#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from .baseclass import BaseClass


#--------------------------------------------------------------------------------
# 이벤트 핸들러.
#--------------------------------------------------------------------------------
class EventHandler(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__callbacks: Set[Callable[..., None]]


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, callbacks: Optional[List[Callable[..., None]]] = None) -> None:
		thisInstance.__callbacks = set()
		if callbacks:
			thisInstance.__callbacks.update(callbacks)


	#--------------------------------------------------------------------------------
	# 전체 제거.
	#--------------------------------------------------------------------------------
	def Clear(thisInstance) -> None:
		thisInstance.__callbacks.clear()


	#--------------------------------------------------------------------------------
	# 추가.
	#--------------------------------------------------------------------------------
	def Add(thisInstance, callback: Callable[..., None]) -> None:
		if thisInstance.Contains(callback):
			return
		thisInstance.__callbacks.add(callback)


	#--------------------------------------------------------------------------------
	# 제거.
	#--------------------------------------------------------------------------------
	def Remove(thisInstance, callback: Callable[..., None]) -> None:
		if not thisInstance.Contains(callback):
			return
		thisInstance.__callbacks.remove(callback)


	#--------------------------------------------------------------------------------
	# 포함 여부.
	#--------------------------------------------------------------------------------
	def Contains(thisInstance, callback: Callable[..., None]) -> bool:
		if callback not in thisInstance.__callbacks:
			return False
		return True


	#--------------------------------------------------------------------------------
	# 등록된 함수 실행.
	#--------------------------------------------------------------------------------
	def Execute(thisInstance, *argumentTuple, **argumentDictionary) -> None:
		for callable in thisInstance.__callbacks:
			callable(*argumentTuple, **argumentDictionary)