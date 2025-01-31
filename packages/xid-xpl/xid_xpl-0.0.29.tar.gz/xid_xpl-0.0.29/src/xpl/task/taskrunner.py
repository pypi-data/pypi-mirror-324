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
from queue import Queue
from .task import Task
from .target import Target
from ..environment import ExitCodeType


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
LINEFEED: str = "\n"
READTEXT: str = "rt"
READBINARY: str = "rb"
WRITETEXT: str = "wt"
WRITEBINARY: str = "wb"
UTF8: str = "utf-8"


#--------------------------------------------------------------------------------
# 작업 처리기.
#--------------------------------------------------------------------------------
TTarget = TypeVar("TTarget", bound = Target)
TTask = TypeVar("TTask", bound = Task)
class TaskRunner(Generic[TTarget, TTask]):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__targets: list[TTarget]
	__tasks: list[TTask]


	#--------------------------------------------------------------------------------
	# 대상 갯수 반환.
	#--------------------------------------------------------------------------------
	@property
	def TargetCount(thisInstance) -> int:
		return len(thisInstance.__targets)
	

	#--------------------------------------------------------------------------------
	# 작업 갯수 반환.
	#--------------------------------------------------------------------------------
	@property
	def TaskCount(thisInstance) -> int:
		return len(thisInstance.__tasks)
	

	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		base = super()
		base.__init__()

		thisInstance.__targets = list()
		thisInstance.__tasks = list()
		thisInstance.OnCreate()


	#--------------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __del__(thisInstance) -> None:
		try:
			thisInstance.OnDestroy()
		except Exception as exception:
			raise


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnCreate(thisInstance) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnDestroy(thisInstance) -> None:
		pass


	#------------------------------------------------------------------------
	# 작업 전체 비우기.
	#------------------------------------------------------------------------
	def ClearTask(thisInstance) -> None:
		thisInstance.__tasks.clear()
			

	#------------------------------------------------------------------------
	# 작업 추가.
	#------------------------------------------------------------------------
	def AddTask(thisInstance, task: TTask) -> bool:
		if not task:
			return False
		if task in thisInstance.__tasks:
			return False
				
		thisInstance.__tasks.append(task)
		return  True


	#------------------------------------------------------------------------
	# 작업 중심의 전체 실행.
	# - 태스크 -> 대상 ... 대상 -> 다음 태스크 -> 대상 ... 대상 -> 다음 태스크 ...
	# - 실패 대상은 탈락.
	#------------------------------------------------------------------------
	def RunAllTasks(thisInstance, *argumentTuple, **argumentDictionary) -> int:
		argumentDictionary["taskRunner"] = thisInstance
		targets: list[TTarget] = argumentDictionary.get("targets")
		activeTargets = list(targets)

		# 큐에 담기.
		taskQueue = Queue()
		for task in thisInstance.__tasks:
			taskQueue.put(task)

		while not taskQueue.empty():
			task = taskQueue.get()
			task = cast(TTask, task)
			for target in activeTargets:
				target = cast(TTarget, targets)
				resultCode = task.Execute(target, *argumentTuple, **argumentDictionary)
				if resultCode != 0:
					thisInstance.ClearTask(True)
					return resultCode
		return 0


	#------------------------------------------------------------------------
	# 대상 중심의 전체 실행.
	# - 대상 전체 -> 태스크 -> 대상 전체 -> 태스크.
	# - 대상 -> 태스크 ... 태스크 -> 다음 대상.
	# - 실패 대상은 탈락.
	#------------------------------------------------------------------------
	def RunAllTargets(thisInstance, *argumentTuple, **argumentDictionary) -> int:
		argumentDictionary["taskRunner"] = thisInstance
		targets: list[TTarget] = argumentDictionary.get("targets")
		activeTargets = list(targets)
		for target in targets:
			target = cast(TTarget, targets)
			for task in thisInstance.__tasks:
				task = cast(TTask, task)
				try:
					resultCode = task.Execute(target, *argumentTuple, **argumentDictionary)
				except Exception as exception:
					return ExitCodeType.GENERAL_ERROR # 일반적 오류.
				if resultCode != 0:
					thisInstance.ClearTask(True)
					return resultCode
		return 0