#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..core import ManagedObject, ManagedObjectGarbageCollection, WeakedReference
from .component import Component


#--------------------------------------------------------------------------------
# 엔티티.
# - 고유식별자를 지니고 있으며 컴포넌트 컨테이너의 역할을 수행.
#--------------------------------------------------------------------------------
T = TypeVar("TComponent", bound = Component)
class Entity(ManagedObject):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__componentIdentifiers: list


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnCreate(thisInstance, *argumentTuple, **argumentDictionary) -> None:
		base = super()
		base.OnCreate(*argumentTuple, **argumentDictionary)
		thisInstance.__componentIdentifiers = list()


	#--------------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnDestroy(thisInstance) -> None:
		for componentIdentifier in thisInstance.__componentIdentifiers:
			ManagedObject.Destroy(componentIdentifier)
		thisInstance.__componentIdentifiers.clear()
		base = super()
		base.OnDestroy()


	#--------------------------------------------------------------------------------
	# 컴포넌트 추가.
	#--------------------------------------------------------------------------------
	def AddComponent(thisInstance, componentType: Type[T], *argumentTuple, **argumentDictionary) -> Optional[WeakedReference[T]]:
		argumentDictionary["ownerIdentifer"] = thisInstance.Identifier
		component: WeakedReference[T] = ManagedObject.Instantiate(componentType, *argumentTuple, **argumentDictionary)
		thisInstance.__componentIdentifiers.append(component.Identifier)
		return component
	

	#--------------------------------------------------------------------------------
	# 컴포넌트 제거.
	#--------------------------------------------------------------------------------
	def RemoveCompoent(thisInstance, componentType: Type[T]) -> bool:
		for componentIdentifier in thisInstance.__componentIdentifiers:
			obj: ManagedObject = ManagedObjectGarbageCollection.Find(componentIdentifier)
			if not obj:
				continue
			if not isinstance(obj, componentType):
				continue
			ManagedObject.Destroy(obj)
			thisInstance.__componentIdentifiers.remove(componentIdentifier)
			return True
		return False
	

	#--------------------------------------------------------------------------------
	# 컴포넌트 반환.
	#--------------------------------------------------------------------------------
	def GetComponent(thisInstance, componentType: Type[T]) -> Optional[WeakedReference[T]]:
		for componentIdentifier in thisInstance.__componentIdentifiers:
			component: WeakedReference[T] = ManagedObjectGarbageCollection.FindWeakedReference(componentIdentifier)
			if component:
				return component
		return None