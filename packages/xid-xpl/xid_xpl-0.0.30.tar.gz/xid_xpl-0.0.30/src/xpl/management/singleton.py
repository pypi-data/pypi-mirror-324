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
from threading import Lock
from ..console import Console
from ..core import BaseClass
from ..exception import SingletonError


#--------------------------------------------------------------------------------
# 싱글톤 클래스.
# - 이 클래스를 상속 받은 클래스는 외부에서 생성자를 호출해서 할당하려고 하면 예외가 발생한다.
# - 또한 GetInstance() 에서 멀티쓰레드 안정성 확보를 위해 약간의 지연이 있다.
# - DerivedClass(Singleton): pass
# - DerivedClass.GetInstance() # OK
# - newInstance = DerivedClass() # ERROR: SingletonException
#--------------------------------------------------------------------------------
TSingleton = TypeVar("TSingleton", bound = "Singleton")
class Singleton(BaseClass, Generic[TSingleton]):
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__Instance: TSingleton = None
	__IsLocked: bool = True
	__ThreadLock: Lock = Lock()


	#--------------------------------------------------------------------------------
	# 인스턴스 할당.
	#--------------------------------------------------------------------------------
	def __new__(thisClassType: Type[TSingleton]) -> TSingleton:
		# 인스턴스 명시적 생성시 예외 처리.
		if thisClassType.__IsLocked:
			raise SingletonError("Cannot create instance directly. Use GetInstance() instead.")

		# 생성.
		thisClassType.__Instance = super(Singleton, thisClassType).__new__(thisClassType)
		return thisClassType.__Instance


	#--------------------------------------------------------------------------------
	# 인스턴스 파괴.
	#--------------------------------------------------------------------------------
	def __del__(thisInstance) -> None:
		# 인스턴스 삭제시 예외 처리.
		raise SingletonError("Cannot delete singleton instance.")


	#--------------------------------------------------------------------------------
	# 인스턴스 반환.
	# - 없으면 생성해서 반환.
	#--------------------------------------------------------------------------------
	@classmethod
	def GetInstance(thisClassType: Type[TSingleton]) -> TSingleton:
		with thisClassType.__ThreadLock:
			if not thisClassType.__Instance:
				thisClassType.__IsLocked = False
				thisClassType.__Instance = thisClassType()
				thisClassType.__IsLocked = True
		return thisClassType.__Instance