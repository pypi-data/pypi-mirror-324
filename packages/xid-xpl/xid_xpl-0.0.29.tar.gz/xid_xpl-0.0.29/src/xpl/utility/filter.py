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
# 필터 클래스.
#--------------------------------------------------------------------------------
T = TypeVar("T")
class Filter(Generic[T]):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__iterable: Iterable[T]
	__predicate: Callable[[T], bool]


	#--------------------------------------------------------------------------------
	# 반복자가 반복하기 위해 반복 될 수 있는 대상 목록.
	#--------------------------------------------------------------------------------
	@property
	def Iterable(thisInstance) -> Iterable[T]:
		return thisInstance.__iterable

	#--------------------------------------------------------------------------------
	# 반복자가 반복하기 위해 반복 될 수 있는 대상 목록.
	#--------------------------------------------------------------------------------
	@Iterable.setter
	def Iterable(thisInstance, iterable: Iterable[T]) -> None:
		thisInstance.__iterable = iterable


	#--------------------------------------------------------------------------------
	# 조건 평가를 위한 함수 객체.
	# - None이면 조건 평가를 하지 않고 무조건 True.
	#--------------------------------------------------------------------------------
	@property
	def Predicate(thisInstance) -> Callable[[T], bool]:
		return thisInstance.__predicate


	#--------------------------------------------------------------------------------
	# 조건 평가를 위한 함수 객체.
	# - None이면 조건 평가를 하지 않고 무조건 True.
	#--------------------------------------------------------------------------------
	@Predicate.setter
	def Predicate(thisInstance, predicate: Callable[[T], bool]) -> None:
		thisInstance.__predicate = predicate


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance):
		thisInstance.__iterable = None
		thisInstance.__predicate = None


	#--------------------------------------------------------------------------------
	# 반복문 순회.
	#--------------------------------------------------------------------------------
	def __iter__(thisInstance) -> Iterator[T]:
		if thisInstance.__predicate:
			for item in thisInstance.__iterable:
				if thisInstance.__predicate(item):
					yield item
		else:
			for item in thisInstance.__iterable:
				yield item