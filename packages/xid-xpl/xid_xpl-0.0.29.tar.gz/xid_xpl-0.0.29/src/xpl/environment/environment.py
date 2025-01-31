#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import platform
import subprocess
from .platformtype import PlatformType


#--------------------------------------------------------------------------------
# 현재 시스템 환경 정보.
#--------------------------------------------------------------------------------
class Environment:
	#--------------------------------------------------------------------------------
	# 현재 시스템의 플랫폼 타입 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetPlatformType() -> PlatformType:
		systemName: str = platform.system()
		systemName = systemName.upper()
		if systemName == "WINDOWS":
			return PlatformType.WINDOWS
		elif systemName == "DARWIN":
			return PlatformType.MACOS
		elif systemName == "LINUX":
			return PlatformType.LINUX
		else:
			return PlatformType.UNKNOWN
		

	#--------------------------------------------------------------------------------
	# 현재 시스템에 설치된 파이썬 목록을 별도 콘솔에서 조회하여 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetPythonInterpreters() -> list[str]:
		try:
			platformType: PlatformType = Environment.GetPlatformType()
			if platformType == PlatformType.WINDOWS:
				output: str = subprocess.check_output("where python", shell = True, text = True)
			else:
				output: str = subprocess.check_output("which -a python python3", shell = True, text = True)
			interpreters: list[str] = output.strip().split("\n")
			return interpreters
		except Exception as exception:
			return list()