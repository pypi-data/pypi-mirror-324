#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..core import BaseClass, Meta


#--------------------------------------------------------------------------------
# 공유 클래스의 메타클래스 (클래스 타입 클래스).
#--------------------------------------------------------------------------------
class MetaClass(Meta):
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__Instances: Dict[Type[MetaClass], SharedClass] = dict()


	#--------------------------------------------------------------------------------
	# 호출 프로토콜 메서드.
	# - 인스턴스 할당 요청 됨(생성자 호출됨).
	#--------------------------------------------------------------------------------
	def __call__(thisClassType, *argumentTuple: Any, **kwds: Any) -> Any:
		if thisClassType in thisClassType.__Instances:
			instance = thisClassType.__Instances[thisClassType]
			return instance
		else:
			base = super()
			instance = base.__call__(*argumentTuple, **kwds)
			thisClassType.__Instances[thisClassType] = instance

			
#--------------------------------------------------------------------------------
# 공유 클래스 (싱글톤 클래스).
# - 어디서 생성해도 항상 같은 인스턴스를 반환.
# - class ChildClass(SharedClass): pass
# - value1 = ChildClass()
# - value2 = ChildClass()
# - value1 == value2
#--------------------------------------------------------------------------------
TSharedClass = TypeVar("TSharedClass", bound = "SharedClass")
class SharedClass(BaseClass, metaclass = MetaClass):
	#--------------------------------------------------------------------------------
	# 인스턴스 반환.
	# - 없으면 생성해서 반환.
	#--------------------------------------------------------------------------------
	@classmethod
	def GetSharedInstance(thisClassType: Type[TSharedClass]) -> TSharedClass:
		return thisClassType()