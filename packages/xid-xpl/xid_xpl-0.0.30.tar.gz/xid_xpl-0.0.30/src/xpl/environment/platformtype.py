#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from enum import Enum, auto


#--------------------------------------------------------------------------------
# 플랫폼 타입.
#--------------------------------------------------------------------------------
class PlatformType(Enum):
	UNKNOWN = auto()
	
	# windows.
	WINDOWS = auto()

	# linux.
	LINUX = auto()
	ANDROID = auto()
	STEAMOS = auto()

	# apple.
	MACOS = auto()
	IOS = auto()
	IPADOS = auto()
	WATCHOS = auto()
	TVOS = auto()
	VISIONOS = auto()

	# web.
	WEBGL = auto()
	WEBGPU = auto()