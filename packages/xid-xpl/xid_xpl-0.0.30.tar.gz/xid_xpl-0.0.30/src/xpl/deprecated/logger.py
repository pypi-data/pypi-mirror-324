#------------------------------------------------------------------------
# 참조 목록.
#------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from ..console import Console
from ..utility import StringUtility, TIMESTAMP_DEFUALT, TIMESTAMP_SIMPLE


#------------------------------------------------------------------------
# 전역 상수 목록.
#------------------------------------------------------------------------
EMPTY: str = ""
SPACE: str = " "
FILE_WRITETEXT: str = "wt"
APPENDTEXT: str = "at"
UTF8: str = "utf-8"
TAB: str = "\t"
LINEFEED: str = "\n"


#------------------------------------------------------------------------
# 기록 처리기.
#------------------------------------------------------------------------
class Logger:
	#------------------------------------------------------------------------
	# 멤버 변수 목록.
	#------------------------------------------------------------------------
	__texts: list[str]


	#------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		thisInstance.__texts: list[str] = list()
		thisInstance.Clear()


	#------------------------------------------------------------------------
	# 비우기.
	#------------------------------------------------------------------------
	def Clear(thisInstance) -> None:
		thisInstance.__texts.clear()


	#------------------------------------------------------------------------
	# 추가.
	#------------------------------------------------------------------------
	def Enqueue(thisInstance, text: str, sections: list[str] = None, indent: int = 0) -> None:
		if not sections:
			sections = list()
		timestamp: str = StringUtility.GetTimestamp(TIMESTAMP_DEFUALT)
		sections.insert(0, timestamp)

		prefixString: str = "\t" * indent
		sectionString: str = EMPTY.join([f"{prefixString}[{section}]" for section in sections])
		result = f"{sectionString}{SPACE}{text}"
		thisInstance.__texts.append(result)
		Console.Print(result)


	#------------------------------------------------------------------------
	# 저장.
	#------------------------------------------------------------------------
	def SaveToFile(thisInstance, filepath: str) -> None:
		with open(filepath, APPENDTEXT, encoding = UTF8) as file:
			text = LINEFEED.join(thisInstance.__texts)
			file.write(text)
			file.write(LINEFEED)
			file.write(LINEFEED)
			thisInstance.Clear()