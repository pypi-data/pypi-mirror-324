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


#--------------------------------------------------------------------------------
# 파이썬 빌트인 함수들을 바탕으로 리플렉션 기능으로 확장한 클래스.
#--------------------------------------------------------------------------------
class Reflection:
	"""파이썬 리플렉션 클래스"""
	#--------------------------------------------------------------------------------
	# 대상이 타입 인스턴스인지 여부 반환.
	# - instance = Hello()
	# - instance: 인스턴스
	# - instance.__class__: 인스턴스의 클래스 타입 (class Hello)
	# - instance.__class__ == Hello: 동일
	#
	# - instance.__class__.__class__: 클래스의 클래스 타입 (class type)
	# - instance.__class__.__class__ == type: 동일
	# - 타입은 "클래스의 메타클래스"로서 클래스는 타입의 인스턴스라고 할 수 있다.
	# - instance < class < type
	# - instance는 type과 직접적인 관련이 없기 때문에 같지 않다.
	#--------------------------------------------------------------------------------
	@staticmethod
	def IsType(target: object) -> bool:
		"""대상이 타입 클래스인지 여부 반환."""
		if not builtins.isinstance(target, builtins.type):
			return False
		return True


	#--------------------------------------------------------------------------------
	# 대상이 클래스 타입에 해당하는 인스턴스인지 여부 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def IsInstanceType(target: object, classType: Type) -> bool:
		"""대상의 타입이 지정 타입과 동일한지 여부 반환."""
		if not builtins.isinstance(target, classType):
			return False
		return True


	#--------------------------------------------------------------------------------
	# 대상이 클래스 타입 목록 중 하나에 해당하는 인스턴스인지 여부 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def IsInstanceInTypes(target: object, classTypes: List[Type]) -> bool:
		"""대상이 타입 중 하나에 속해있는지 여부 반환."""
		if not builtins.isinstance(target, tuple(classTypes)):
			return False
		return True


	#--------------------------------------------------------------------------------
	# 어트리뷰트의 값을 설정. (혹은 생성)
	#--------------------------------------------------------------------------------
	@staticmethod
	def SetAttributeValue(target: object, attributeName: str, value: Any, allowCreation: bool = True) -> bool:
		"""대상의 어트리뷰트를 설정. 어트리뷰트가 없다면 새로 추가."""
		realAttributeName = Reflection.GetAttributeName(target, attributeName)
		if realAttributeName:
			builtins.setattr(target, attributeName, value)
			return True
		elif allowCreation:
			builtins.setattr(target, attributeName, value)
			return True
		else:
			return False

	#--------------------------------------------------------------------------------
	# 어트리뷰트 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateAttribute(target: object, attributeName: str, attributeValue: Any) -> bool:
		"""대상에게 어트리뷰트를 추가."""
		realAttributeName = Reflection.GetAttributeName(target, attributeName)
		if realAttributeName:
			return False	
		builtins.setattr(target, attributeName, attributeValue)
		return True
	

	#--------------------------------------------------------------------------------
	# 어트리뷰트 제거.
	#--------------------------------------------------------------------------------
	@staticmethod
	def DeleteAttribute(target: object, attributeName: str) -> bool:
		"""대상의 어트리뷰트를 제거."""
		attributeName = Reflection.GetAttributeName(target, attributeName)
		if not attributeName:
			return False	
		builtins.delattr(attributeName)
		return True


	#--------------------------------------------------------------------------------
	# 실제 어트리뷰트 이름 반환.
	# - 입력값에서 대소문자가 다르더라도 실제 어트리뷰트이름이 있다면 반환.
	# - 존재한다면 실제 어트리뷰트 이름을 반환. (입력값과 동일할 수도 다를 수도 있음)
	# - 존재하지 않으면 빈문자열 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetAttributeName(target: object, attributeName: str) -> str:
		"""대상에게 어트리뷰트가 존재하면 그 이름을 반환하고 없으면 빈문자열 반환. (입력값과 같을 수도 다를 수도 있음)"""
		if not target:
			return str()
		if not attributeName:
			return str()
		attributeNameLower: str = attributeName.lower()
		for attributeName in builtins.dir(target):
			realAttributeNameLower: str = attributeName.lower()
			if attributeNameLower == realAttributeNameLower:
				return attributeName				
		return str()


	#--------------------------------------------------------------------------------
	# 어트리뷰트의 값을 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetAttributeValue(target: object, attributeName: str, defaultValue: Any = None) -> Any:
		"""대상의 어트리뷰트를 반환"""
		if not target:
			return defaultValue
		if not attributeName:
			return defaultValue
		attributeName: str = Reflection.GetAttributeName(target, attributeName)
		if not attributeName:
			return defaultValue
		attributeValue: Any = builtins.getattr(target, attributeName)
		return attributeValue

	#--------------------------------------------------------------------------------
	# 어트리뷰트의 타입을 반환.
	# - 값으로부터 추론하므로 값이 없을 경우는 NoneType이다.
	# - 파이썬은 동적타이핑 언어라서 이렇게 되었을 경우 얻어올 수 있는 방법은 없다.
	# - 파이랜스 같은 인텔리센스는 타입힌팅을 통해 코드에디터레벨에서 정적타이핑인 척만 할 뿐이다.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetAttributeType(target: object, attributeName: str) -> type:
		"""대상이 어트리뷰트를 가지고 있는지 여부 반환"""
		if not Reflection.HasAttribute(attributeName):
			return None
		attributeValue = Reflection.GetAttributeValue(target, attributeName)
		return type(attributeValue)
	

	#--------------------------------------------------------------------------------
	# 어트리뷰트의 존재 유무 판단.
	#--------------------------------------------------------------------------------
	@staticmethod
	def HasAttribute(target: object, attributeName: str) -> bool:
		"""대상이 어트리뷰트를 가지고 있는지 여부 반환"""
		if not target:
			return False
		if not attributeName:
			return False
		attributeName: str = Reflection.GetAttributeName(target, attributeName)
		if not attributeName:
			return False
		return True