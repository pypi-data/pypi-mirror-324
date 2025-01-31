#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..console import Console
from .baseagent import BaseAgent as Agent


#--------------------------------------------------------------------------------
# 기본 컴포넌트.
#--------------------------------------------------------------------------------
class BaseBehaviour(Agent):
	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnCreate(thisInstance) -> None:
		pass

	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnDestroy(thisInstance) -> None:
		pass