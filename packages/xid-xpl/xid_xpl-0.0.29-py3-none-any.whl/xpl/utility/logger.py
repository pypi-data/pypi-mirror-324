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
from enum import Enum
import logging
from logging import Logger as PythonStandardLogger
from logging import StreamHandler, FileHandler, Formatter
from logging.handlers import QueueHandler, QueueListener
import os
from queue import Queue
# from asyncio import Queue
from ..environment import Path
from .loglevel import LogLevel



#--------------------------------------------------------------------------------
# 로그 클래스.
#--------------------------------------------------------------------------------
class Logger:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__name: str
	__filePath: str
	__level: LogLevel
	__logger: PythonStandardLogger
	__consoleHandler: StreamHandler
	__fileHandler: FileHandler
	__formatter: Formatter
	# __queue: Queue
	# __queueHandler: QueueHandler
	# __queueListener: QueueListener


	#--------------------------------------------------------------------------------
	# 로거 이름.
	#--------------------------------------------------------------------------------
	@property
	def Name(thisInstance) -> str:
		return thisInstance.__name
	

	#--------------------------------------------------------------------------------
	# 로그 파일 위치.
	#--------------------------------------------------------------------------------
	@property
	def FilePath(thisInstance) -> str:
		return thisInstance.__filePath


	#--------------------------------------------------------------------------------
	# 로그 수준.
	#--------------------------------------------------------------------------------
	@property
	def Level(thisInstance) -> LogLevel:
		return thisInstance.__level


	#--------------------------------------------------------------------------------
	# 프로세스 아이디.
	#--------------------------------------------------------------------------------
	@property
	def ProcessID(thisInstance) -> int:
		return os.getpid()
	

	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	# - 로그파일을 None 을 입력하면 
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, name: str, filePath: str, level: LogLevel = LogLevel.DEBUG, 
			  useShowProcessID: bool = False, useShowName: bool = False) -> None:
		thisInstance.__name = name
		thisInstance.__filePath = filePath
		thisInstance.__level = level
	
		# 이름이 없다면 파일명에서 이름을 가져옴.
		if not name:
			if not filePath:
				raise NameError(name)
			else:
				_, fileName = Path.GetPathAndFileNameFromFileFullPath(filePath)
				name = os.path.splitext(fileName)

		thisInstance.__logger: PythonStandardLogger = logging.getLogger(name)
		thisInstance.__logger.setLevel(level.value)

		# 포맷 설정.
		if useShowProcessID:
			if useShowName:
				thisInstance.__formatter = Formatter("[%(asctime)s][%(name)s][%(process)d][%(levelname)s]%(message)s")
			else:
				thisInstance.__formatter = Formatter("[%(asctime)s][%(process)d][%(levelname)s]%(message)s")
		else:
			if useShowName:
				thisInstance.__formatter = Formatter("[%(asctime)s][%(name)s][%(process)d][%(levelname)s]%(message)s")
			else:
				thisInstance.__formatter = Formatter("[%(asctime)s][%(process)d][%(levelname)s]%(message)s")

		# 콘솔 로그.
		thisInstance.__consoleHandler = StreamHandler()
		thisInstance.__consoleHandler.setLevel(level.value)
		thisInstance.__consoleHandler.setFormatter(thisInstance.__formatter)
		thisInstance.__logger.addHandler(thisInstance.__consoleHandler) # 큐 핸들러 사용시 제외.

		# 파일 로그.
		if filePath:
			thisInstance.__fileHandler = FileHandler(filePath)
			thisInstance.__fileHandler.setLevel(level.value)
			thisInstance.__fileHandler.setFormatter(thisInstance.__formatter)
			thisInstance.__logger.addHandler(thisInstance.__fileHandler) # 큐 핸들러 사용시 제외.

		# # 큐 로그.
		# thisInstance.__queue = Queue()
		# thisInstance.__queueHandler = QueueHandler(thisInstance.__queue)
		# thisInstance.__logger.addHandler(thisInstance.__queueHandler)

		# # 큐 리스너.
		# handlers = list()
		# handlers.append(thisInstance.__consoleHandler)
		# if filePath:
		# 	handlers.append(thisInstance.__fileHandler)
		# thisInstance.__queueListener = QueueListener(thisInstance.__queue, *handlers)
		# thisInstance.__queueListener.start()


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def __Log(thisInstance, level: LogLevel, message: object) -> None:
		if isinstance(message, str):
			if not message.startswith("["):
				message = f" {message}"
		else:
			text = str(message)
			if not text.startswith("["):
				message = f" {text}"

		thisInstance.__logger.log(level.value, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogDebug(thisInstance, message: object) -> None:
		thisInstance.__Log(LogLevel.DEBUG, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogInfo(thisInstance, message: object) -> None:
		thisInstance.__Log(LogLevel.INFO, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogWarning(thisInstance, message: object) -> None:
		thisInstance.__Log(LogLevel.WARNING, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogError(thisInstance, message: object) -> None:
		thisInstance.__Log(LogLevel.ERROR, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogException(thisInstance, message: object, *argumentTuple) -> None:
		thisInstance.__logger.exception(message, *argumentTuple, True, True, 8)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogCritical(thisInstance, message: object) -> None:
		thisInstance.__Log(LogLevel.CRITICAL, message)