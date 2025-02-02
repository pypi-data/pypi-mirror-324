#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..ecs import Entity


#------------------------------------------------------------------------
# 전역 상수 목록.
#------------------------------------------------------------------------
LINEFEED: str = "\n"
FILE_READTEXT: str = "rt"
FILE_READBINARY: str = "rb"
FILE_WRITETEXT: str = "wt"
FILE_WRITEBINARY: str = "wb"
UTF8: str = "utf-8"
TAB: str = "\t"


#------------------------------------------------------------------------
# 작업 대상.
#------------------------------------------------------------------------
class Target(Entity):
	#------------------------------------------------------------------------
	# 멤버 변수 목록.
	#------------------------------------------------------------------------


	#------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#------------------------------------------------------------------------
	def OnCreate(thisInstance, *argumentTuple, **argumentDictionary) -> None:
		base = super()
		base.OnCreate(*argumentTuple, **argumentDictionary)
		

	#------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#------------------------------------------------------------------------
	def OnDestroy(thisInstance) -> None:
		base = super()
		base.OnDestroy()


	#------------------------------------------------------------------------
	# 시작됨.
	#------------------------------------------------------------------------
	def OnStart(thisInstance, task: Entity) -> None:
		return


	#------------------------------------------------------------------------
	# 종료됨.
	#------------------------------------------------------------------------
	def OnComplete(thisInstance, task: Entity, resultCode: int) -> None:
		return 0