#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..console.console import Console
from .baseclass import BaseClass


#--------------------------------------------------------------------------------
# 노드 클래스.
#--------------------------------------------------------------------------------
TNode = TypeVar("TNode", bound = "BaseNode")
class BaseNode(BaseClass, Generic[TNode]):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__parent: TNode
	__children: list[TNode]
	__isAlive: bool
	__name: str


	#--------------------------------------------------------------------------------
	# 부모 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Parent(thisInstance) -> TNode:
		return thisInstance.__parent


	#--------------------------------------------------------------------------------
	# 부모 프로퍼티 설정.
	#--------------------------------------------------------------------------------
	@Parent.setter
	def Parent(thisInstance, parent: TNode) -> None:
		if thisInstance.__parent is parent:
			return		
		if thisInstance.__parent:
			thisInstance.__parent.RemoveChild(thisInstance)
		thisInstance.__parent = parent
		if thisInstance.__parent:
			thisInstance.__parent.AddChild(thisInstance)


	#--------------------------------------------------------------------------------
	# 자식 프로퍼티 반환. (신규 리스트 생성 후 얕은 복사로 반환되므로 수정 불가)
	#--------------------------------------------------------------------------------
	@property
	def Children(thisInstance) -> list[TNode]:
		return list(thisInstance.__children)


	#--------------------------------------------------------------------------------
	# 이름 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Name(thisInstance) -> str:
		return thisInstance.__name


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, name: str, **argumentDictionary) -> None:
		base = super()
		base.__init__()
		thisInstance.__children = list()
		thisInstance.__isAlive = True
		thisInstance.__name = name
		base.__dict__.update(**argumentDictionary)


	#--------------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __del__(thisInstance) -> None:
		base = super()
		base.__del__()
		

	#--------------------------------------------------------------------------------
	# 자식 추가.
	#--------------------------------------------------------------------------------
	def AddChild(thisInstance, child: TNode) -> None:
		if child in thisInstance.__children:
			return
		
		thisInstance.__children.append(child)
		child.__parent = thisInstance


	#--------------------------------------------------------------------------------
	# 자식 제거.
	#--------------------------------------------------------------------------------
	def RemoveChild(thisInstance, child: TNode) -> None:
		if child not in thisInstance.__children:
			return
		thisInstance.__children.remove(child)
		child.__parent = None


	#--------------------------------------------------------------------------------
	# 형제 노드 순서 설정.
	#--------------------------------------------------------------------------------
	def SetSiblingByIndex(thisInstance, index: int, newSibling: TNode) -> None:
		siblings = thisInstance.GetSiblings()
		if index < 0 or index >= len(siblings):
			raise IndexError("Sibling index out of range.")
		thisInstance.__parent.__children[thisInstance.__parent.__children.index(siblings[index])] = newSibling
		newSibling.Parent = thisInstance.__parent


	#--------------------------------------------------------------------------------
	# 형제 목록 반환.
	#--------------------------------------------------------------------------------
	def GetSiblings(thisInstance) -> list[TNode]:
		if thisInstance.__parent is None:
			return list()
		return [child for child in thisInstance.__parent.Children if child != thisInstance]


	#--------------------------------------------------------------------------------
	# 순서에 대한 형제 노드 반환
	#--------------------------------------------------------------------------------
	def GetSiblingByIndex(thisInstance, index: int) -> TNode:
		siblings = thisInstance.GetSiblings()
		if index < 0 or index >= len(siblings):
			raise IndexError("Sibling index out of range.")
		return siblings[index]


	#--------------------------------------------------------------------------------
	# 조상 노드 찾기.
	# - path는 노드이름들로 엮인 경로이다.
	#--------------------------------------------------------------------------------
	def FindAncestor(thisInstance, path: str) -> TNode:
		parts = path.split("/")
		current: TNode = thisInstance
		for part in reversed(parts):
			if part == ".":
				continue
			if current is None or current.Name != part:
				return None
			current = current.Parent
		return current


	#--------------------------------------------------------------------------------
	# 형제 노드 찾기.
	#--------------------------------------------------------------------------------
	def FindSibling(thisInstance, name: str) -> TNode:
		for sibling in thisInstance.GetSiblings():
			if sibling.Name == name:
				return sibling
		return None


	#--------------------------------------------------------------------------------
	# 자손 노드 찾기.
	#--------------------------------------------------------------------------------
	def FindDescendant(thisInstance, path: str) -> TNode:
		parts: list[str] = path.split("/")
		current: TNode = thisInstance
		for part in parts:
			if part == ".":
				continue
			found = False
			for child in current.Children:
				if child.Name == part:
					current = child
					found = True
					break
			if not found:
				return None
		return current


	#--------------------------------------------------------------------------------
	# 복제.
	#--------------------------------------------------------------------------------
	def Clone(thisInstance) -> TNode:
		clonedNode: TNode = TNode(thisInstance.Name, thisInstance.__dict__)
		return clonedNode


	#--------------------------------------------------------------------------------
	# 파괴.
	#--------------------------------------------------------------------------------
	def Destroy(thisInstance) -> None:
		if thisInstance.__isAlive:
			return
		thisInstance.__isAlive = False
		for child in list(thisInstance.__children):
			child.Destroy()
		if thisInstance.__parent:
			thisInstance.__parent.RemoveChild(thisInstance)
			thisInstance.__parent = None
		thisInstance.__children.clear()


	#--------------------------------------------------------------------------------
	# 반복문 순회.
	#--------------------------------------------------------------------------------
	def __iter__(thisInstance) -> Iterator:
		yield thisInstance
		for child in thisInstance.__children:
			yield from iter(child)


	#--------------------------------------------------------------------------------
	# 대상 노드의 구조를 자신에게로 덮어쓰기.
	#--------------------------------------------------------------------------------
	def CopyStructure(thisInstance, sourceNode: TNode) -> None:
		thisInstance.Name = sourceNode.Name
		# thisInstance.__dict__.update(sourceNode.__dict__)
		for child in sourceNode.Children:
			newChild: TNode = TNode(child.Name, child.__dict__)
			newChild.CopyStructure(child)
			thisInstance.AddChild(newChild)


	#--------------------------------------------------------------------------------
	# 문자열 변환.
	#--------------------------------------------------------------------------------
	def __repr__(thisInstance) -> str:
		base = super()
		return base.__repr__()