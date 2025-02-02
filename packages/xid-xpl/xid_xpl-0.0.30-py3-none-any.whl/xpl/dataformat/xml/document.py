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
# import html
import os
import re
from xml.dom import minidom as Minidom
from xml.dom.minidom import Document as MinidomDocument
from xml.etree import ElementTree as XMLDocument
from xml.etree.ElementTree import Element as XMLElement
from .element import Element
from ...utility import XMLUtility


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"
UTF8: str = "utf-8"
EMPTY: str = ""
RE_REMOVE_NS0: str = "(ns0:|ns0|:ns0)"
RE_REMOVE_TABANDLINEFEED: str = "^\t+$\n"
RE_REMOVE_LINEFEED: str = "^\n"
LINEFEED: str = "\n"


#--------------------------------------------------------------------------------
# XML 문서.
# - 실제로는 XMLDocument의 래퍼.
#--------------------------------------------------------------------------------
class Document:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__xmlDocument: XMLDocument


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
	def RootXMLElement(thisInstance) -> XMLElement:
		rootXMLElement: XMLElement = thisInstance.XMLDocument.getroot()
		return rootXMLElement
	

	#--------------------------------------------------------------------------------
	# XML 루트 요소 프로퍼티.
	#--------------------------------------------------------------------------------
	@RootXMLElement.setter
	def RootXMLElement(thisInstance, rootXMLElement: XMLElement) -> None:
		try:
			thisInstance.XMLDocument._setroot(rootXMLElement)
		except Exception as exception:
			raise
	

	#--------------------------------------------------------------------------------
	# 루트 요소 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def RootElement(thisInstance) -> Element:
		rootElement: XMLElement = thisInstance.RootXMLElement
		return Element.CreateFromXMLElement(rootElement)
	

	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, xmlDocument: XMLDocument) -> None:
		thisInstance.__xmlDocument = xmlDocument


	#--------------------------------------------------------------------------------
	# 문자열 변환 오퍼레이터 메서드.
	#--------------------------------------------------------------------------------
	def __str__(thisInstance) -> str:
		return thisInstance.SaveToString()


	#--------------------------------------------------------------------------------
	# 제대로 된 XML 도큐먼트인지 여부.
	#--------------------------------------------------------------------------------
	def IsValid(thisInstance) -> bool:
		if thisInstance.__xmlDocument == None:
			return False
		return True
	

	#--------------------------------------------------------------------------------
	# 문자열에서 불러오기.
	#--------------------------------------------------------------------------------
	def LoadFromString(thisInstance, xmlString: str) -> bool:
		if not xmlString:
			return False
		
		xmlDocument: XMLDocument = XMLDocument.fromstring(xmlString)
		thisInstance.__xmlDocument = xmlDocument
		return True
	

	#--------------------------------------------------------------------------------
	# 파일에서 불러오기.
	#--------------------------------------------------------------------------------
	def LoadFromXMLFile(thisInstance, xmlFilePath: str) -> bool:
		if not xmlFilePath:
			return False
		if not os.path.isfile(xmlFilePath):
			raise False
		xmlDocument: XMLDocument = XMLDocument.parse(xmlFilePath)
		thisInstance.__xmlDocument = xmlDocument
		return True


	#--------------------------------------------------------------------------------
	# 문자열로 저장하기.
	#--------------------------------------------------------------------------------
	def SaveToString(thisInstance) -> str:
		if not thisInstance.IsValid():
			return str()
		
		# XML 데이터를 문자열로 변환.
		xmlBytes: bytes = XMLDocument.tostring(thisInstance.RootXMLElement, xml_declaration = False, encoding = UTF8)
		xmlString = xmlBytes.decode(UTF8)

		# 문자열을 미니돔 도큐먼트로 변환.
		minidomDocument: MinidomDocument = Minidom.parseString(xmlString)
		xmlString = minidomDocument.toprettyxml()

		# NS0이 붙어있거나, 탭만 있는 라인은 제거.
		xmlString = re.sub(RE_REMOVE_NS0, EMPTY, xmlString)
		xmlString = re.sub(RE_REMOVE_TABANDLINEFEED, EMPTY, xmlString, flags = re.MULTILINE)
		xmlString = re.sub(RE_REMOVE_LINEFEED, EMPTY, xmlString, flags = re.MULTILINE)
		# xmlString = html.unescape(xmlString) # HTML에서 사용할 수 있는 모든 엔티티문자열 &<...>; 변환.
		xmlString = XMLUtility.EntitiesToString(xmlString)

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
		if not isOverwrite:
			if os.path.isfile(xmlFilePath):
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
	def Create() -> Document:
		return Document(None)
	

	#--------------------------------------------------------------------------------
	# 비어있는 객체 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFromXMLDocument(xmlDocument: XMLDocument) -> Document:
		return Document(xmlDocument)


	#--------------------------------------------------------------------------------
	# 비어있는 객체 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFromXMLElement(xmlElement: XMLElement) -> Document:
		xmlDocument = XMLDocument(xmlElement)
		return Document(xmlDocument)
	

	#--------------------------------------------------------------------------------
	# 문자열로 객체 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFromString(xmlString: str) -> Document:
		document: Document = Document.Create()
		document.LoadFromString(xmlString)
		return document


	#--------------------------------------------------------------------------------
	# 파일로 객체 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFromXMLFile(xmlFilePath: str) -> Document:
		if not xmlFilePath:
			return False
		if not os.path.isfile(xmlFilePath):
			raise FileNotFoundError(xmlFilePath)

		document: Document = Document.Create()
		if not document.LoadFromXMLFile(xmlFilePath):
			raise Exception()
		return document
	

	# #------------------------------------------------------------------------
	# # XML에 사용자 정의 엔티티 정의.
	# # - 스펙상 사용자 정의 엔티티는 .xml의 DOCTYPE 혹은 외부 DTD파일에 정의하고 참조.
	# # - SetCustomEntities는 XML 안에 정의.
	# #------------------------------------------------------------------------
	# @staticmethod
	# def SetCustomEntities(document: Document, namespaces: Dict[str, str] = None) -> str:
	# 	doctypeElement: Element = document.RootElement.Find(".\\DOCTYPE", namespaces)
	# 	if not doctypeElement:
	# 		return ""
		
