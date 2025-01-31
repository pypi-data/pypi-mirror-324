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
from xml.etree.ElementTree import Element as XMLElement
from ..console import Console


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
XMLNAMESPACE: str = "xmlns"
OPENINGCURLYBRACE: str = "{"
CLOSINGCURLYBRACE: str = "}"


#--------------------------------------------------------------------------------
# 요소.
#--------------------------------------------------------------------------------
class LazyXMLElement:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__xmlElement: XMLElement


	# #--------------------------------------------------------------------------------
	# # XML 부모 요소 프로퍼티.
	# #--------------------------------------------------------------------------------
	# @property
	# def Parent(thisInstance) -> LazyXMLElement:
	# 	thisInstance.__xmlElement.
	

	#--------------------------------------------------------------------------------
	# 네임스페이스 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Namespace(thisInstance) -> str:
		tag, namespace = LazyXMLElement.GetTagAndNamespaceFromElement(thisInstance.__xmlElement)
		return namespace
		

	#--------------------------------------------------------------------------------
	# 네임스페이스 프로퍼티.
	#--------------------------------------------------------------------------------
	@Namespace.setter
	def Namespace(thisInstance, value: str) -> None:
		tag, namespace = LazyXMLElement.GetTagAndNamespaceFromElement(thisInstance.__xmlElement)
		# 추가 or 수정.
		if value:
			thisInstance.__xmlElement.tag = f"{{{value}}}{thisInstance.__xmlElement.tag.split(CLOSINGCURLYBRACE)[-1]}"
		# 제거.
		elif namespace:
			thisInstance.__xmlElement.tag = thisInstance.__xmlElement.tag.split(CLOSINGCURLYBRACE)[-1]


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, tag: str, internalElement: Optional[XMLElement] = None, **argumentDictionary) -> None:
		if thisInstance.__xmlElement != None:
			thisInstance.__xmlElement = internalElement
		else:
			thisInstance.__xmlElement = XMLElement(tag, **argumentDictionary)


	#--------------------------------------------------------------------------------
	# 자식 추가.
	#--------------------------------------------------------------------------------
	def AddChild(thisInstance, element: LazyXMLElement) -> None:
		thisInstance.__xmlElement.append(element)


	#--------------------------------------------------------------------------------
	# 자식 제거.
	#--------------------------------------------------------------------------------
	def RemoveChild(thisInstance, element: LazyXMLElement) -> None:
		thisInstance.__xmlElement.remove(element)


	#--------------------------------------------------------------------------------
	# 모든 자식 제거.
	#--------------------------------------------------------------------------------
	def RemoveAllChildren(thisInstance) -> None:
		thisInstance.__xmlElement.clear()


	#--------------------------------------------------------------------------------
	# 자식 찾기.
	#--------------------------------------------------------------------------------
	def FindChild(thisInstance, path: str, namespaces: Optional[Dict[str, str]]) -> Optional[LazyXMLElement]:
		child: XMLElement = thisInstance.__xmlElement.find(path, namespaces)
		if child == None:
			return None
		child = cast(XMLElement, child)


	#--------------------------------------------------------------------------------
	# 모든 자식 찾기.
	#--------------------------------------------------------------------------------
	def FindAllChildren(thisInstance, path: str, namespaces: Optional[Dict[str, str]]) -> List[LazyXMLElement]:
		children = list()
		for child in thisInstance.__xmlElement.findall(path, namespaces):
			child = cast(XMLElement, child)
			element = LazyXMLElement.CreateElement(child)
			children.append(element)
		return children


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateElement(tag: str, element: XMLElement = None, **argumentDictionary) -> LazyXMLElement:
		return LazyXMLElement(tag, element, **argumentDictionary)
	

	#--------------------------------------------------------------------------------
	# 태그에서 이름과 네임스페이스를 분리.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetTagAndNamespaceFromElement(element: XMLElement) -> Tuple[str, str]:
		if CLOSINGCURLYBRACE in element.tag:
			namespace, tag = element.tag[1:].split(CLOSINGCURLYBRACE)
			return tag, namespace
		else:
			return element.tag, str()