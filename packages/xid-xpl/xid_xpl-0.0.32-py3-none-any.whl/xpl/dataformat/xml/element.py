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
from .path import Path
from ...core import Reflection


#--------------------------------------------------------------------------------
# XML 요소.
# - 실제로는 XMLElement의 래퍼.
#--------------------------------------------------------------------------------
class Element:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__xmlElement: XMLElement


	#--------------------------------------------------------------------------------
	# 엘리먼트 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def XMLElement(thisInstance) -> XMLElement:
		return thisInstance.__xmlElement


	#--------------------------------------------------------------------------------
	# 엘리먼트 프로퍼티.
	#--------------------------------------------------------------------------------
	@XMLElement.setter
	def XMLElement(thisInstance, value: XMLElement) -> None:
		thisInstance.__xmlElement = value


	#--------------------------------------------------------------------------------
	# 자식 요소 목록 프로퍼티. (새로운 컨테이너 생성하여 반환됨)
	#--------------------------------------------------------------------------------
	@property
	def Children(thisInstance) -> List[Element]:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")
		children = list()
		for xmlElement in list(thisInstance.XMLElement):
			xmlElement = cast(XMLElement, xmlElement)
			element = Element.CreateFromXMLElement(xmlElement)
			children.append(element)
		return children
	

	#--------------------------------------------------------------------------------
	# 텍스트 값 프로퍼티.
	# - 값이 있을 경우 반환 값의 타입은 str이며 값 자체가 없을 경우 None 반환.
	#--------------------------------------------------------------------------------
	@property
	def Text(thisInstance) -> Optional[str]:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")
		return thisInstance.XMLElement.text


	#--------------------------------------------------------------------------------
	# 텍스트 값 프로퍼티.
	# - None 설정은 값의 제거와 동일하므로 빈 문자열로 남길 때는 "" 필요.
	#--------------------------------------------------------------------------------
	@Text.setter
	def Text(thisInstance, value: str) -> None:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")
		elif value is None:
			thisInstance.XMLElement.text = None
		elif builtins.isinstance(value, str):
			thisInstance.XMLElement.text = value
		else:
			raise ValueError(value)


	#--------------------------------------------------------------------------------
	# 텍스트 값 프로퍼티.
	# - 아예 제거할 경우.
	#--------------------------------------------------------------------------------
	@Text.deleter
	def Text(thisInstance) -> None:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")
		thisInstance.XMLElement.text = None


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, xmlElement: XMLElement) -> None:
		thisInstance.__xmlElement = xmlElement


	#--------------------------------------------------------------------------------
	# 제대로 된 XML 엘리먼트인지 여부.
	#--------------------------------------------------------------------------------
	def IsValid(thisInstance) -> bool:
		if thisInstance.XMLElement == None:
			return False
		return True
	

	#--------------------------------------------------------------------------------
	# 텍스트 값 보유 여부 반환.
	# - 빈 문자열도 일단 값이 있는 것으로 판단.
	#--------------------------------------------------------------------------------
	def HasText(thisInstance) -> bool:
		if not thisInstance.IsValid():
			return False
		if thisInstance.XMLElement.text == None:
			return False
		return True


	#--------------------------------------------------------------------------------
	# 속성 설정.
	#--------------------------------------------------------------------------------
	def AddOrSetAttribute(thisInstance, name: str, value: Any) -> None:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")	

		thisInstance.XMLElement.set(name, value)
		# thisInstance.XMLElement.attrib[name] = value


	#--------------------------------------------------------------------------------
	# 속성 제거.
	#--------------------------------------------------------------------------------
	def RemoveAttribute(thisInstance, name: str) -> bool:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")	
		if not thisInstance.HasAttribute(name):
			return False
		del thisInstance.XMLElement.attrib[name]
		return True


	#--------------------------------------------------------------------------------
	# 속성 존재 여부 반환.
	#--------------------------------------------------------------------------------
	def HasAttribute(thisInstance, name: str) -> bool:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")
		if name not in thisInstance.XMLElement.attrib:
			return False
		return True


	#--------------------------------------------------------------------------------
	# 속성 가져오기.
	#--------------------------------------------------------------------------------
	def GetAttribute(thisInstance, name: str, default: Optional[Any] = None) -> Any:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")	
		return thisInstance.XMLElement.attrib.get(name, default)


	#--------------------------------------------------------------------------------
	# 자식 요소 추가.
	#--------------------------------------------------------------------------------
	def AddChild(thisInstance, element: Element) -> None:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")
		thisInstance.XMLElement.append(element.XMLElement)
	

	#--------------------------------------------------------------------------------
	# 자식 요소 삭제.
	#--------------------------------------------------------------------------------
	def RemoveChild(thisInstance, element: Element) -> None:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")
		thisInstance.XMLElement.remove(element)


	#--------------------------------------------------------------------------------
	# 자식 요소 전체 삭제.
	#--------------------------------------------------------------------------------
	def RemoveAllChildren(thisInstance) -> None:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")
		thisInstance.XMLElement.clear()


	#--------------------------------------------------------------------------------
	# 요소 검색하여 단일 개체 반환.
	#--------------------------------------------------------------------------------
	def Find(thisInstance, path: Union[Path, str], namespaces: Optional[Dict[str, str]] = None) -> Optional[Element]:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")	
		if Reflection.IsInstanceType(path, Path):
			path = cast(Path, path)
			path = str(path)
			xmlElement: XMLElement = thisInstance.XMLElement.find(path, namespaces)
			return Element.CreateFromXMLElement(xmlElement)
		elif Reflection.IsInstanceType(path, str):
			path = cast(str, path)
			xmlElement: XMLElement = thisInstance.XMLElement.find(path, namespaces)
			return Element.CreateFromXMLElement(xmlElement)
		return None


	#--------------------------------------------------------------------------------
	# 요소 검색하여 목록으로 반환.
	#--------------------------------------------------------------------------------
	def FindAll(thisInstance, path: Union[Path, str], namespaces: Optional[Dict[str, str]] = None) -> List[Element]:
		if not thisInstance.IsValid():
			raise ValueError("XMLElement is None")	
		elements = list()
		if path is Path:
			path = cast(Path, path)
			path = str(path)
			for xmlElement in thisInstance.XMLElement.findall(path, namespaces):
				xmlElement: XMLElement = cast(XMLElement, xmlElement)
				element: Element = Element.CreateFromXMLElement(xmlElement)
				elements.append(element)
		elif path is str:
			path = cast(str, path)
			for xmlElement in thisInstance.XMLElement.findall(path, namespaces):
				xmlElement: XMLElement = cast(XMLElement, xmlElement)
				element: Element = Element.CreateFromXMLElement(xmlElement)
				elements.append(element)
		return elements


	#--------------------------------------------------------------------------------
	# 새 객체 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Create() -> Element:
		element = Element(None)
		return element


	#--------------------------------------------------------------------------------
	# 새 객체 생성. (값이 존재할 경우)
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFromValue(tag: str, attributes: dict = {}, **extraAttributes) -> Element:
		xmlElement = XMLElement(tag, attributes, **extraAttributes)
		return Element(xmlElement)
	

	#--------------------------------------------------------------------------------
	# 새 객체 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFromXMLElement(xmlElement: XMLElement) -> Element:
		return Element(xmlElement)