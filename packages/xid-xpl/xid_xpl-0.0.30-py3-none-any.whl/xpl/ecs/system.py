#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..core import ManagedObject, WeakedReference


#--------------------------------------------------------------------------------
# 처리기 객체.
# - 엔티티 목록을 받아 해당 엔티티 내의 컴포넌트들을 컨트롤하는 구조.
#--------------------------------------------------------------------------------
class System(ManagedObject):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnCreate(thisInstance, *argumentTuple, **argumentDictionary) -> None:
		base = super()
		base.OnCreate(*argumentTuple, **argumentDictionary)


	#--------------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnDestroy(thisInstance) -> None:
		base = super()
		base.OnDestroy()


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def Execute(thisInstance, *argumentTuple, **argumentDictionary) -> Any:
		pass