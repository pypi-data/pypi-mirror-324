#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload



#--------------------------------------------------------------------------------
# XML 유틸리티.
#--------------------------------------------------------------------------------
class XMLUtility:
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__XMLEntities: Dict[str, str] = {
		"&lt;": "<",
		"&gt;": ">",
		"&amp;": "&",
		"&quot;": '"',
		"&apos;": "'",
	}


	#------------------------------------------------------------------------
	# XML 문자열에 포함된 엔티티를 모두 문자열로 변환하여 반환.
	#------------------------------------------------------------------------
	@classmethod
	def EntitiesToString(thisClassType, xmlString: str) -> str:
		for entity, string in thisClassType.__XMLEntities.items():
			xmlString = xmlString.replace(entity, string)
		return xmlString