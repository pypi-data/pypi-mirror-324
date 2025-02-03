#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from enum import Enum
from ..core import BaseNode


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY: str = ""


#--------------------------------------------------------------------------------
# 타입 별칭 정의 목록.
#--------------------------------------------------------------------------------
NodeEventFunction = Callable[..., Any] # function은 3.10에 존재하지 않음.


#--------------------------------------------------------------------------------
# 노드 이벤트 타입.
#--------------------------------------------------------------------------------
class NodeEventType(Enum):
	CREATEEVENT = "__OnCreateEvent" # callable[[None], None]
	DESTROYEVENT = "__OnDestroyEvent" # callable[[None], None]
	PARENTCHANGEEVENT = "__OnParentChangeEvent" # callable[[Node, Node], None]
	SIBLINGCHANGEEVENT = "__OnSiblingChangeEvent" # callable[[Node], None]
	CHILDCHANGEEVENT = "__OnChildChangeEvent" # callable[[Node], None]


#--------------------------------------------------------------------------------
# 노드 클래스.
#--------------------------------------------------------------------------------
class EventNode(BaseNode):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__events: dict[NodeEventType, set[NodeEventFunction]]
	__value: Any


	#--------------------------------------------------------------------------------
	# 값 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Value(thisInstance) -> Any:
		return thisInstance.__value


	#--------------------------------------------------------------------------------
	# 값 프로퍼티 설정.
	#--------------------------------------------------------------------------------
	@property.setter
	def Value(thisInstance, value: Any) -> None:
		thisInstance.__value = value



	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, name: str, value: Any = None) -> None:
		base = super()
		base.__init__(name)
		
		thisInstance.__value = value

		# 이벤트 목록 초기화.
		for nodeEventType in NodeEventType:
			thisInstance.__events[nodeEventType] = set()
		thisInstance.__events[NodeEventType.CREATEEVENT].add(thisInstance.__OnCreateEvent)
		thisInstance.__events[NodeEventType.DESTROYEVENT].add(thisInstance.__OnDestroyEvent)
		thisInstance.__events[NodeEventType.PARENTCHANGEEVENT].add(thisInstance.__OnParentChangeEvent)
		thisInstance.__events[NodeEventType.SIBLINGCHANGEEVENT].add(thisInstance.__OnSiblingChangeEvent)
		thisInstance.__events[NodeEventType.CHILDCHANGEEVENT].add(thisInstance.__OnChildChangeEvent)

		# 생성 이벤트.
		thisInstance.NotifyEvent(NodeEventType.CREATEEVENT)


	#--------------------------------------------------------------------------------
	# 자식 추가.
	#--------------------------------------------------------------------------------
	def AddChild(thisInstance, child: BaseNode) -> None:
		base = super()
		base.AddChild(child)

		# 자식 변경 이벤트.
		thisInstance.NotifyEvent(NodeEventType.CHILDCHANGEEVENT, child)


	#--------------------------------------------------------------------------------
	# 자식 제거.
	#--------------------------------------------------------------------------------
	def RemoveChild(thisInstance, child: BaseNode) -> None:
		base = super()
		base.RemoveChild(child)

		# 자식 변경 이벤트.
		thisInstance.NotifyEvent(NodeEventType.CHILDCHANGEEVENT, child)


	#--------------------------------------------------------------------------------
	# 형제 노드 순서 설정.
	#--------------------------------------------------------------------------------
	def SetSiblingByIndex(thisInstance, index: int, newSibling: BaseNode) -> None:
		siblings = thisInstance.GetSiblings()
		if index < 0 or index >= len(siblings):
			raise IndexError("Sibling index out of range.")
		thisInstance.__parent.__children[thisInstance.__parent.__children.index(siblings[index])] = newSibling
		newSibling.Parent = thisInstance.__parent

		# 형제 변경 이벤트.
		thisInstance.NotifyEvent(NodeEventType.SIBLINGCHANGEEVENT, newSibling)



	#--------------------------------------------------------------------------------
	# 형제 노드 찾기.
	#--------------------------------------------------------------------------------
	def FindSibling(thisInstance, name: str) -> BaseNode:
		for sibling in thisInstance.GetSiblings():
			if sibling.Name == name:
				return sibling
		return None


	#--------------------------------------------------------------------------------
	# 파괴.
	#--------------------------------------------------------------------------------
	def Destroy(thisInstance, ) -> None:
		if thisInstance.__isAlive:
			return
		thisInstance.__isAlive = False

		thisInstance.NotifyEvent(NodeEventType.DESTROYEVENT)
		for child in list(thisInstance.__children):
			child.Destroy()
		if thisInstance.__parent:
			thisInstance.__parent.RemoveChild(thisInstance)
			thisInstance.__parent = None
		thisInstance.__children.clear()


	#--------------------------------------------------------------------------------
	# 노드가 생성됨.
	#--------------------------------------------------------------------------------
	def __OnCreateEvent(thisInstance) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 노드가 파괴됨.
	#--------------------------------------------------------------------------------
	def __OnDestroyEvent(thisInstance) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 부모 노드가 변경됨.
	#--------------------------------------------------------------------------------
	def __OnParentChangeEvent(thisInstance, previouslyParentNode: BaseNode, nextParentNode: BaseNode) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 형제 노드가 변경됨.
	#--------------------------------------------------------------------------------
	def __OnSiblingChangeEvent(thisInstance, siblingNode: BaseNode) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 자식 노드가 변경됨.
	#--------------------------------------------------------------------------------
	def __OnChildChangeEvent(thisInstance, childNode: BaseNode) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 이벤트 통지.
	#--------------------------------------------------------------------------------
	def NotifyEvent(thisInstance, nodeEventType: str, *argumentTuple, **argumentDictionary) -> None:
		for callback in thisInstance.__events[nodeEventType]:
			if not callback:
				continue
			callback(*argumentTuple, **argumentDictionary)


	#--------------------------------------------------------------------------------
	# 전체 이벤트 초기화.
	# - 전체를 초기화하지만 함수 목록 객체 자체를 삭제하진 않는다.
	#--------------------------------------------------------------------------------
	def ClearAllEvents(thisInstance) -> None:
		for nodeEventType, callbacks in thisInstance.__events.items():
			callbacks.clear()


	#--------------------------------------------------------------------------------
	# 이벤트 초기화.
	#--------------------------------------------------------------------------------
	def ClearEvent(thisInstance, nodeEventType: NodeEventType) -> None:
		callbacks = thisInstance.__events[nodeEventType]
		callbacks.clear()


	#--------------------------------------------------------------------------------
	# 이벤트 재설정.
	#--------------------------------------------------------------------------------
	def SetEvent(thisInstance, nodeEventType: NodeEventType, nodeEvent: NodeEventFunction) -> None:
		events = thisInstance.__events[nodeEventType]
		events.clear()
		events.update(nodeEvent)


	#--------------------------------------------------------------------------------
	# 이벤트 추가.
	#--------------------------------------------------------------------------------
	def AddEvent(thisInstance, nodeEventType: NodeEventType, nodeEvent: NodeEventFunction) -> None:
		events = thisInstance.__events[nodeEventType]
		if nodeEvent not in events:
			events.update(nodeEvent)


	#--------------------------------------------------------------------------------
	# 이벤트 제거.
	#--------------------------------------------------------------------------------
	def RemoveEvent(thisInstance, nodeEventType: NodeEventType, nodeEvent: NodeEventFunction) -> None:
		events = thisInstance.__events[nodeEventType]
		events.discard(nodeEvent)