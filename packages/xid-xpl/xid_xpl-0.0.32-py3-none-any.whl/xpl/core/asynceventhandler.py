#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import asyncio
from .baseclass import BaseClass


#--------------------------------------------------------------------------------
# 비동기 이벤트 핸들러.
#--------------------------------------------------------------------------------
class AsyncEventHandler(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__callbacks: Set[Callable[..., Awaitable[None]]]


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, callbacks: Optional[List[Callable[..., Awaitable[None]]]] = None) -> None:
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
	def Add(thisInstance, callable: Callable[..., Awaitable[None]]) -> None:
		if thisInstance.Contains(callable):
			return
		thisInstance.__callbacks.add(callable)


	#--------------------------------------------------------------------------------
	# 제거.
	#--------------------------------------------------------------------------------
	def Remove(thisInstance, callable: Callable[..., Awaitable[None]]) -> None:
		if not thisInstance.Contains(callable):
			return
		thisInstance.__callbacks.remove(callable)


	#--------------------------------------------------------------------------------
	# 포함 여부.
	#--------------------------------------------------------------------------------
	def Contains(thisInstance, callback: Callable[..., Awaitable[None]]) -> bool:
		if callback not in thisInstance.__callbacks:
			return False
		return True


	#--------------------------------------------------------------------------------
	# 등록된 비동기 함수 실행.
	#--------------------------------------------------------------------------------
	async def Execute(thisInstance, *argumentTuple, **argumentDictionary) -> None:
		tasks: List[Awaitable] = list()
		for callback in thisInstance.__callbacks:
			awaitable: Awaitable = callback(*argumentTuple, **argumentDictionary)
			tasks.append(awaitable)
		# asyncio.gather는 개별인자로 테스크를 취급하므로 언패킹해서 집어넣음.
		await asyncio.gather(*tasks)