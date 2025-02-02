#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from uuid import UUID, uuid4
from .baseclass import BaseClass
from .weakedreference import WeakedReference


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
T = TypeVar("T", bound = "ManagedObject")


#--------------------------------------------------------------------------------
# 관리된 오브젝트.
#--------------------------------------------------------------------------------
class ManagedObject(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__identifier: str


	#--------------------------------------------------------------------------------
	# 인스턴스 고유 식별자.
	#--------------------------------------------------------------------------------
	@property
	def Identifier(thisInstance) -> str:
		return thisInstance.__identifier


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, *argumentTuple, **argumentDictionary):
		try:
			base = super()
			base.__init__()

			unique: UUID = uuid4()
			# thisInstance.__identifier = str(unique) # 550e8400-e29b-41d4-a716-446655440000
			thisInstance.__identifier = str(unique.hex) # 550e8400e29b41d4a716446655440000
			thisInstance.OnCreate(*argumentTuple, **argumentDictionary)
		except Exception as exception:
			raise


	#--------------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __del__(thisInstance) -> None:
		try:
			thisInstance.OnDestroy()

			# base = super()
			# base.__del__()
		except Exception as exception:
			raise


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnCreate(thisInstance, *argumentTuple, **argumentDictionary) -> None:
		return


	#--------------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnDestroy(thisInstance) -> None:
		return
	

	#--------------------------------------------------------------------------------
	# 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Instantiate(referenceType: Type[T], *argumentTuple, **argumentDictionary) -> WeakedReference[T]:
		obj: T = referenceType(*argumentTuple, **argumentDictionary)
		ManagedObjectGarbageCollection.Register(obj.Identifier, obj)
		weakedReference: WeakedReference[T] = ManagedObjectGarbageCollection.FindWeakedReference(referenceType, obj.Identifier)
		return weakedReference


	#--------------------------------------------------------------------------------
	# 검색.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Find(identifier: str) -> ManagedObject:
		obj: ManagedObject = ManagedObjectGarbageCollection.Find(identifier)
		return obj
	
	#--------------------------------------------------------------------------------
	# 검색.
	#--------------------------------------------------------------------------------
	@staticmethod
	def FindObject(identifier: str) -> WeakedReference[ManagedObject]:
		weakedReference: WeakedReference[ManagedObject] = ManagedObject.FindObjectOfType(ManagedObject, identifier)
		return weakedReference
	

	#--------------------------------------------------------------------------------
	# 검색.
	#--------------------------------------------------------------------------------
	@staticmethod
	def FindObjectOfType(referenceType: Type[T], identifier: str) -> WeakedReference[T]:
		weakedReference: WeakedReference[T] = ManagedObjectGarbageCollection.FindWeakedReference(referenceType, identifier)
		return weakedReference
	

	#--------------------------------------------------------------------------------
	# 파괴.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Destroy(obj: ManagedObject) -> None:
		ManagedObjectGarbageCollection.Unregister(obj)


#--------------------------------------------------------------------------------
# 매니지드 오브젝트 가비지 컬렉션. (내부 관리용)
#--------------------------------------------------------------------------------
class ManagedObjectGarbageCollection(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Objects: dict[str, ManagedObject] = dict()


	#--------------------------------------------------------------------------------
	# 갯수 프로퍼티.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Count() -> int:
		return len(ManagedObjectGarbageCollection.Objects)


	#--------------------------------------------------------------------------------
	# 전체 제거.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Cleanup() -> bool:
		if not ManagedObjectGarbageCollection.Objects:
			return False		
		ManagedObjectGarbageCollection.Objects.clear()
		return True	
	

	#--------------------------------------------------------------------------------
	# 추가.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Register(obj: ManagedObject) -> bool:
		if not obj:
			return False		
		if obj.Identifier in ManagedObjectGarbageCollection.Objects:
			return False
		ManagedObjectGarbageCollection.Objects[obj.Identifier] = obj
		return True	


	#--------------------------------------------------------------------------------
	# 제거.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Unregister(identifier: str) -> bool:
		if identifier not in ManagedObjectGarbageCollection.Objects:
			return False		
		del ManagedObjectGarbageCollection.Objects[identifier]
		return True


	#--------------------------------------------------------------------------------
	# 포함 여부.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Contains(identifier: str) -> bool:
		if identifier not in ManagedObjectGarbageCollection.Objects:
			return False
		return True
	

	#--------------------------------------------------------------------------------
	# 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Find(identifier: str) -> ManagedObject:
		if identifier not in ManagedObjectGarbageCollection.Objects:
			return None
		obj: ManagedObject = ManagedObjectGarbageCollection.Objects[identifier]
		return obj


	#--------------------------------------------------------------------------------
	# 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def FindWeakedReference(referenceType: Type[T], identifier: str) -> Optional[WeakedReference[T]]:
		obj: ManagedObject = ManagedObjectGarbageCollection.Find(identifier)
		if not obj:
			return None
		if not isinstance(obj, referenceType):
			return None		
		weakedReference: WeakedReference[T] = WeakedReference[T](obj)
		return weakedReference