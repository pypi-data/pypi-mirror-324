#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..core import ManagedObject, WeakedReference


#--------------------------------------------------------------------------------
# 기본 기능 객체.
# - 특정 데이터와 기능을 보유하고 엔티티에 종속되는 객체.
#--------------------------------------------------------------------------------
class Component(ManagedObject):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__ownerIdentifer: str


	#--------------------------------------------------------------------------------
	# 소유자 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Owner(thisInstance) -> WeakedReference[ManagedObject]:
		return ManagedObject.FindObject(thisInstance.__ownerIdentifer)


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnCreate(thisInstance, *argumentTuple, **argumentDictionary) -> None:
		base = super()
		base.OnCreate(*argumentTuple, **argumentDictionary)
		thisInstance.__ownerIdentifer = argumentDictionary.get("ownerIdentifer")


	#--------------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnDestroy(thisInstance) -> None:
		base = super()
		base.OnDestroy()
