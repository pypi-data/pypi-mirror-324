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
import os
import re
from xml.dom import minidom as Minidom
from xml.dom.minidom import Document as MinidomDocument
from xml.etree import ElementTree as XMLDocument
from .lazyxmlelement import LazyXMLElement


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"
UTF8: str = "utf-8"
WIX: str = "wix"
EMPTY: str = ""
RE_REMOVE_NS0: str = "(ns0:|ns0|:ns0)"
RE_REMOVE_TABANDLINEFEED: str = "^\t+$\n"
RE_REMOVE_LINEFEED: str = "^\n"
LINEFEED: str = "\n"


#--------------------------------------------------------------------------------
# 문서.
#--------------------------------------------------------------------------------
class LazyXMLDocument():
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__xmlDocument: XMLDocument
	__cacheElements: List[LazyXMLElement]


	#--------------------------------------------------------------------------------
	# XML 트리 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def XMLDocument(thisInstance) -> XMLDocument:
		return thisInstance.__xmlDocument


	#--------------------------------------------------------------------------------
	# XML 루트 요소 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Root(thisInstance) -> LazyXMLElement:
		element: LazyXMLElement = LazyXMLElement.CreateElement(thisInstance.__xmlDocument.getroot())
		return element


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, elementTree: XMLDocument = None) -> None:
		thisInstance.__xmlDocument = elementTree


	#--------------------------------------------------------------------------------
	# 문자열 변환 오퍼레이터.
	#--------------------------------------------------------------------------------
	def __str__(thisInstance) -> str:
		return thisInstance.SaveToString()


	#--------------------------------------------------------------------------------
	# 제대로 된 XML 도큐먼트인지 여부.
	#--------------------------------------------------------------------------------
	def IsValid(thisInstance) -> bool:
		if not thisInstance.__xmlDocument:
			return False
		return True
	

	#--------------------------------------------------------------------------------
	# 문자열에서 불러오기.
	#--------------------------------------------------------------------------------
	def LoadFromString(thisInstance, xmlString: str) -> bool:
		if not xmlString:
			return False
		thisInstance.__xmlDocument = XMLDocument.fromstring(xmlString)
		return True
	

	#--------------------------------------------------------------------------------
	# 파일에서 불러오기.
	#--------------------------------------------------------------------------------
	def LoadFromFile(thisInstance, xmlFilePath: str) -> bool:
		if not xmlFilePath:
			return False
		if not os.path.isfile(xmlFilePath):
			raise False
		thisInstance.__xmlDocument = XMLDocument.parse(xmlFilePath)
		return True


	#--------------------------------------------------------------------------------
	# 문자열로 저장하기.
	#--------------------------------------------------------------------------------
	def SaveToString(thisInstance) -> str:
		if not thisInstance.IsValid():
			return str()
		
		# XML 데이터를 문자열로 변환.
		xmlBytes: bytes = XMLDocument.tostring(thisInstance.Root, xml_declaration = False, encoding = UTF8)
		xmlString = xmlBytes.decode(UTF8)

		# 문자열을 미니돔 도큐먼트로 변환.
		minidomDocument: MinidomDocument = Minidom.parseString(xmlString)
		xmlString = minidomDocument.toprettyxml()

		# NS0이 붙어있거나, 탭만 있는 라인은 제거.
		xmlString = re.sub(RE_REMOVE_NS0, EMPTY, xmlString)
		xmlString = re.sub(RE_REMOVE_TABANDLINEFEED, EMPTY, xmlString, flags = re.MULTILINE)
		xmlString = re.sub(RE_REMOVE_LINEFEED, EMPTY, xmlString, flags = re.MULTILINE)

		# 마지막 개행문자 제거.
		if xmlString.endswith(LINEFEED):
			xmlString = xmlString[:-1]

		return xmlString


	#--------------------------------------------------------------------------------
	# 파일로 저장하기.
	#--------------------------------------------------------------------------------
	def SaveToFile(thisInstance, xmlFilePath: str, isOverwrite: bool = True) -> bool:
		if not xmlFilePath:
			return False
		if not isOverwrite and os.path.isfile(xmlFilePath):
			raise False

		# 저장.
		xmlString: str = thisInstance.SaveToString()
		with builtins.open(xmlFilePath, mode = FILE_WRITETEXT, encoding = UTF8) as outputFile:
			outputFile.write(xmlString)
		return True


	#--------------------------------------------------------------------------------
	# 비어있는 객체 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Create() -> LazyXMLDocument:
		return LazyXMLDocument()
	

	#--------------------------------------------------------------------------------
	# 문자열로 객체 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFromString(xmlString: str) -> LazyXMLDocument:
		document: LazyXMLDocument = LazyXMLDocument.Create()
		document.LoadFromString(xmlString)
		return LazyXMLDocument()


	#--------------------------------------------------------------------------------
	# 파일로 객체 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFromFile(xmlFilePath: str) -> LazyXMLDocument:
		if not xmlFilePath:
			return False
		if not os.path.isfile(xmlFilePath):
			raise FileNotFoundError(xmlFilePath)

		document: LazyXMLDocument = LazyXMLDocument.Create()
		document.LoadFromFile(xmlFilePath)
		return document	