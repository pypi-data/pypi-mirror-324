#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from enum import Enum
from ..console import Console
from ..core import BaseClass


#--------------------------------------------------------------------------------
# 노드 클래스.
#--------------------------------------------------------------------------------
class BaseNode(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__parent: BaseNode
	__children: list[BaseNode]
	__isAlive: bool
	__name: str


	#--------------------------------------------------------------------------------
	# 부모 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Parent(thisInstance) -> BaseNode:
		return thisInstance.__parent


	#--------------------------------------------------------------------------------
	# 부모 프로퍼티 설정.
	#--------------------------------------------------------------------------------
	@Parent.setter
	def Parent(thisInstance, parent: BaseNode) -> None:
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
	def Children(thisInstance) -> list[BaseNode]:
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
		
		thisInstance.__parent = None
		thisInstance.__children = list()
		thisInstance.__isAlive = True
		thisInstance.__name = name


	#--------------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __del__(thisInstance) -> None:
		base = super()
		base.__del__()
		

	#--------------------------------------------------------------------------------
	# 자식 추가.
	#--------------------------------------------------------------------------------
	def AddChild(thisInstance, child: BaseNode) -> None:
		if child in thisInstance.__children:
			return
		
		thisInstance.__children.append(child)
		child.__parent = thisInstance


	#--------------------------------------------------------------------------------
	# 자식 제거.
	#--------------------------------------------------------------------------------
	def RemoveChild(thisInstance, child: BaseNode) -> None:
		if child not in thisInstance.__children:
			return
		thisInstance.__children.remove(child)
		child.__parent = None


	#--------------------------------------------------------------------------------
	# 형제 노드 순서 설정.
	#--------------------------------------------------------------------------------
	def SetSiblingByIndex(thisInstance, index: int, newSibling: BaseNode) -> None:
		siblings = thisInstance.GetSiblings()
		if index < 0 or index >= len(siblings):
			raise IndexError("Sibling index out of range.")
		thisInstance.__parent.__children[thisInstance.__parent.__children.index(siblings[index])] = newSibling
		newSibling.Parent = thisInstance.__parent


	#--------------------------------------------------------------------------------
	# 형제 목록 반환.
	#--------------------------------------------------------------------------------
	def GetSiblings(thisInstance) -> list[BaseNode]:
		if thisInstance.__parent is None:
			return list()
		return [child for child in thisInstance.__parent.Children if child != thisInstance]


	#--------------------------------------------------------------------------------
	# 순서에 대한 형제 노드 반환
	#--------------------------------------------------------------------------------
	def GetSiblingByIndex(thisInstance, index: int) -> BaseNode:
		siblings = thisInstance.GetSiblings()
		if index < 0 or index >= len(siblings):
			raise IndexError("Sibling index out of range.")
		return siblings[index]


	#--------------------------------------------------------------------------------
	# 조상 노드 찾기.
	#--------------------------------------------------------------------------------
	def FindAncestor(thisInstance, path: str) -> BaseNode:
		parts = path.split("/")
		current: BaseNode = thisInstance
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
	def FindSibling(thisInstance, name: str) -> BaseNode:
		for sibling in thisInstance.GetSiblings():
			if sibling.Name == name:
				return sibling
		return None


	#--------------------------------------------------------------------------------
	# 자손 노드 찾기.
	#--------------------------------------------------------------------------------
	def FindDescendant(thisInstance, path: str) -> BaseNode:
		parts: list[str] = path.split("/")
		current: BaseNode = thisInstance
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
	def Clone(thisInstance) -> BaseNode:
		clonedNode = BaseNode(thisInstance.Name, thisInstance.Value)
		for child in thisInstance.Children:
			clonedChild = child.Clone()
			clonedNode.AddChild(clonedChild)
		return clonedNode


	#--------------------------------------------------------------------------------
	# 파괴.
	#--------------------------------------------------------------------------------
	def Destroy(thisInstance, ) -> None:
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
	# 다른 노드의 구조를 복제.
	#--------------------------------------------------------------------------------
	def CopyStructure(thisInstance, otherNode: BaseNode) -> None:
		thisInstance.Name = otherNode.Name
		thisInstance.Value = otherNode.Value
		for child in otherNode.Children:
			newChild = BaseNode(child.Name, child.Value)
			thisInstance.AddChild(newChild)
			newChild.CopyStructure(child)


	#--------------------------------------------------------------------------------
	# 문자열 변환.
	#--------------------------------------------------------------------------------
	def __repr__(thisInstance) -> str:
		return f"Node(Name={thisInstance.Name}, Value={thisInstance.Value})"