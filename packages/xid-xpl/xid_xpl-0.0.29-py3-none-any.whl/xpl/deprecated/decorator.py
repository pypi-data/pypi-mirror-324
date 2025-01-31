#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import inspect
from functools import wraps
from ..core import Reflection



#--------------------------------------------------------------------------------
# 비공개 메서드를 위한 오버라이드 메서드 데코레이터 (인스턴스메서드 전용).
# - 동일 이름의 자식이 있으면 자식을 호출.
# - 동일 이름의 자식이 없으면 자신을 호출.
# - 최상위 메서드에서만 지정.
#--------------------------------------------------------------------------------
def overridemethod(targetMethod: Callable[..., Any]):
	@wraps(targetMethod)
	def Decorate(thisInstance, *argumentTuple, **argumentDictionary) -> Any:
		# 인자 없음 - 일반 함수 혹은 스태틱메서드 일 경우.
		if not argumentTuple: return targetMethod(*argumentTuple, **argumentDictionary)

		argument = argumentTuple[0]

		# 인자 있음 - 하지만 현재 호출한 메서드의 인스턴스나 현재 호출한 메서드의 클래스가 아닐 경우.
		# if not isinstance(argument, type) and not isinstance(argument, thisInstance.__class__): return targetMethod(*argumentTuple, **argumentDictionary)
		if not Reflection.IsInstanceInTypes(argument, [type, thisInstance.__class__]): return targetMethod(*argumentTuple, **argumentDictionary)

		# 첫번째 인자가 클래스 타입 일 경우 or 인스턴스 일 경우.
		isClassMethod = Reflection.IsInstanceType(argument, type)
		if isClassMethod:
			classType = argumentTuple[0]
		else:
			classType = argumentTuple[0].__class__
	
		# 메서드 이름 룰이 비공개 메서드 일 경우 or 공개 메서드 일 경우.
		methodName = targetMethod.__name__
		isPrivateMethod = methodName.startswith("__") and not methodName.endswith("__")
		if isPrivateMethod:
			methodName = methodName.split("__", 1)[-1]
			methodName = f"_{classType.__name__}__{methodName}"

		# 자식 에게 동일 이름의 함수가 있다면 호출.
		if Reflection.HasAttribute(classType, methodName):
			childMethod = Reflection.GetAttributeValue(classType, methodName)
			if childMethod is not targetMethod:
				return childMethod(*argumentTuple, **argumentDictionary)
			
		# 없으면 자신의 함수 호출.
		return targetMethod(*argumentTuple, **argumentDictionary)
	return Decorate


#--------------------------------------------------------------------------------
# 자식의 메소드가 오버라이드 한 것일 때 부모의 동일한 메소드를 대신 호출 해주는 함수.
#--------------------------------------------------------------------------------
def basemethod(thisInstance, *argumentTuple, **argumentDictionary) -> Any:
	currentFrame = inspect.currentframe()
	previouslyFrame = inspect.getouterframes(currentFrame)[1]
	methodName = previouslyFrame.function
	parentClass = thisInstance.__class__.__bases__[0]

	# 비공개 메서드 이름 장식 처리
	isPrivateMethod = methodName.startswith("__") and not methodName.endswith("__")
	if isPrivateMethod:
		methodName = methodName.split("__", 1)[-1]
		methodName = f"_{parentClass.__name__}__{methodName}"

	# 부모 클래스의 메서드를 가져와 호출
	if Reflection.HasAttribute(parentClass, methodName):
		parentMethod = Reflection.GetAttributeValue(parentClass, methodName)
		return parentMethod(thisInstance, *argumentTuple, **argumentDictionary)
	else:
		raise AttributeError(f"{parentClass.__name__} object has no attribute {methodName}")
