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
from ..core import Reflection, BaseClass
# from threading import Lock
# from asyncio import Lock


#--------------------------------------------------------------------------------
# 기본 저장소 클래스.
# - 저장소 클래스를 통해 객체를 호출하면 최초 1회 할당 이후 계속 같은 객체를 반환한다.
# - 저장소 클래스 내부에서 생성되는 탓에 생성시 인자가 없는 객체여야 한다.
# - 만일 생성시 인자가 들어간다면 최초 생성인지 사용자가 판단해서 인자를 넣어주어야 한다.
# - 혹은 Link() 를 통해 외부에서 할당한 인스턴스를 넣어둘 수 있다.
# - 이 클래스를 상속받아서 독자적인 저장소 클래스를 만들 수 있다.
#--------------------------------------------------------------------------------
T = TypeVar("T", bound = Any)
class BaseRepository(BaseClass):
	#--------------------------------------------------------------------------------
	# 저장소에 들어가는 항목.
	#--------------------------------------------------------------------------------
	class RepositoryData(BaseClass):
		#--------------------------------------------------------------------------------
		# 멤버 변수 목록.
		#--------------------------------------------------------------------------------
		type: type
		instance: object


		#--------------------------------------------------------------------------------
		# 초기화 라이프사이클 메서드.
		#--------------------------------------------------------------------------------
		def __init__(thisInstance) -> None:
			base = super()
			base.__init__()
			thisInstance.type = None
			thisInstance.instance = None


	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__IsInitialized: bool = False
	__TargetInstances: Dict[type, RepositoryData] = dict()


	#--------------------------------------------------------------------------------
	# 이벤트 체크.
	#--------------------------------------------------------------------------------
	@classmethod
	def CheckEvent(thisClassType) -> None:
		if not thisClassType.__IsInitialized:
			thisClassType.OnInitialize()
			thisClassType.__IsInitialized = True


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드됨.
	#--------------------------------------------------------------------------------
	@classmethod
	def OnInitialize(thisClassType) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	@classmethod
	def OnFinalize(thisClassType) -> None:
		thisClassType.__TargetInstances.clear()


	#--------------------------------------------------------------------------------
	# 저장소에 모든 인스턴스 제거.
	#--------------------------------------------------------------------------------
	@classmethod
	def Cleanup(thisClassType) -> None:
		thisClassType.CheckEvent()
		thisClassType.__TargetInstances.clear()
	

	#--------------------------------------------------------------------------------
	# 저장소에 기존 인스턴스 설정 (기존 것이 있다면 제거 후 설정).
	#--------------------------------------------------------------------------------
	@classmethod
	def Link(thisClassType, instance: T) -> bool:
		thisClassType.CheckEvent()
		if not instance:
			return False
		
		isType: bool = Reflection.IsInstanceType(instance, type)
		if isType:
			return False

		instanceClassType: Type[T] = instance.__class__
		if instanceClassType in thisClassType.__TargetInstances:
			del thisClassType.__TargetInstances[instanceClassType]
		thisClassType.__TargetInstances[instanceClassType] = instance
		return True
	

	#--------------------------------------------------------------------------------
	# 저장소에 신규 인스턴스 생성 (기존 것이 있다면 제거 후 생성).
	# - 생성자에 값을 넣기 위해 argumentTuple과 argumentDictionary에 값을 넣어주어야 한다.
	# - 물론 값을 넣지 않아도 상관없으며 그 경우 인자 없는 생성자가 호출된다. (생성자에 인자가 존재한다면 주의)
	#--------------------------------------------------------------------------------
	@classmethod
	def Set(thisClassType, targetClassType: Type[T], *argumentTuple: Any, **argumentDictionary: Any) -> T:
		thisClassType.CheckEvent()
		if thisClassType.Contains(targetClassType):
			del thisClassType.__TargetInstances[targetClassType]

		item = BaseRepository.RepositoryData()
		item.type = targetClassType
		item.instance = targetClassType(*argumentTuple, **argumentDictionary)
		thisClassType.__TargetInstances[targetClassType] = item
		return item.instance
	

	#--------------------------------------------------------------------------------
	# 저장소에 존재하는 인스턴스 반환.
	# - 없다면 신규 생성하며 이 때 생성자에 값을 넣기 위해 args와 kwargs 값을 넣어주어야 한다.
	# - 물론 값을 넣지 않아도 상관없으며 그 경우 인자 없는 생성자가 호출된다. 생성자에 인자가 존재한다면 주의)
	#--------------------------------------------------------------------------------
	@classmethod
	def Get(thisClassType, targetClassType: Type[T], *argumentTuple: Any, **argumentDictionary: Any) -> T:
		thisClassType.CheckEvent()
		if thisClassType.Contains(targetClassType):
			item: BaseRepository.RepositoryData = thisClassType.__TargetInstances[targetClassType]
			return item.instance
		else:
			item: BaseRepository.RepositoryData = BaseRepository.RepositoryData()
			item.type = targetClassType
			item.instance = targetClassType(*argumentTuple, **argumentDictionary)
			thisClassType.__TargetInstances[targetClassType] = item
			return item.instance

	#--------------------------------------------------------------------------------
	# 저장소에 해당 인스턴스가 존재하는지 여부.
	#--------------------------------------------------------------------------------
	@classmethod
	def Contains(thisClassType, targetClassType: Type[T]) -> bool:
		thisClassType.CheckEvent()
		if targetClassType not in thisClassType.__TargetInstances:
			return False
		return True
	

	#--------------------------------------------------------------------------------
	# 저장소에 존재하는 인스턴스 반환.
	# - Get과 동일하나 부모를 인자로 넣으면 자식이 있을 경우 그 자식을 가져온다.
	# - 따라서 없으면 자동으로 대상을 추가 할 수가 없어서 안에 없다면 None을 뱉는다.
	#--------------------------------------------------------------------------------
	@classmethod
	def GetInherited(thisClassType, targetClassType: Type[T]) -> T:
		thisClassType.CheckEvent()
		if thisClassType.Contains(targetClassType):
			item: BaseRepository.RepositoryData = thisClassType.__TargetInstances[targetClassType]
			return item.instance
		else:
			for instanceClassType in thisClassType.__TargetInstances:
				if not issubclass(instanceClassType, targetClassType): # instanceClassType의 부모가 targetClassType일 때 참.
					continue
				item: BaseRepository.RepositoryData = thisClassType.__TargetInstances[instanceClassType]
				return item.instance
			return None