#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..console.console import Console


#--------------------------------------------------------------------------------
# 상수 클래스.
#--------------------------------------------------------------------------------
class BaseConstant:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__constantDictionary: Dict[str, Any]


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		thisInstance.__constantDictionary = dict()


	#--------------------------------------------------------------------------------
	# 상수 설정.
	#--------------------------------------------------------------------------------
	def Set(thisInstance, constName: str, constValue: Any) -> None:
		constName = constName.upper()
		if constName in thisInstance.__constantDictionary: 
			raise ValueError(f"Cannot overwrite constant: {constName}")
		thisInstance.__constantDictionary[constName] = constValue


	#--------------------------------------------------------------------------------
	# 상수 반환.
	#--------------------------------------------------------------------------------
	def Get(thisInstance, constName: str) -> Any:
		constName = constName.upper()
		if constName not in thisInstance.__constantDictionary:
			raise KeyError(f"Constant not found: {constName}")
		return thisInstance.__constantDictionary[constName]


	#--------------------------------------------------------------------------------
	# 인스턴스의 멤버 설정.
	#--------------------------------------------------------------------------------
	def __setattr__(thisInstance, name: str, value: Any) -> None:
		# 언더바로 시작하는 멤버 변수는 별도로 할당된 추가 멤버 변수 혹은 클래스 내부 멤버 변수로 가정.
		# 일반적인 set 어트리뷰트로 처리.
		if name.startswith("_"):
			base = super()
			base.__setattr__(name, value)
		# 그 외는 상수로 판정.
		else:
			thisInstance.Set(name, value)


	#--------------------------------------------------------------------------------
	# 인스턴스의 멤버 제거.
	#--------------------------------------------------------------------------------
	def __delattr__(thisInstance, name: str) -> None:
		constName = name.upper()
		if constName in thisInstance.__constantDictionary:
			raise TypeError(f"Cannot delete constant: {constName}")
		

# #--------------------------------------------------------------------------------
# # 모듈에 인스턴스를 할당. (수준 있는 꼼수)
# #--------------------------------------------------------------------------------
# moduleName: str = __name__
# sys.modules[moduleName] = Constant()