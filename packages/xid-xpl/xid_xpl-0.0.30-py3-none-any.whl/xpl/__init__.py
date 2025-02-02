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
# 패키지 포함 목록.
#--------------------------------------------------------------------------------
from .console import Console
from .container import Dictionary
from .core import AnonymousObject, UnnamedClass
from .core import AsyncEventHandler
from .core import BaseClass
from .core import BaseConstant, Constant
from .core import BaseMetaClass, MetaClass, Meta
from .core import BaseNode, Node
from .core import EnumFlag, auto
from .core import EventHandler
from .core import Interface, InterfaceMetaClass, abstractmethod, IInterface, IInterfaceMetaClass, NoInstantiationMetaClass
from .core import ManagedObject, ManagedObjectGarbageCollection
from .core import Reflection
from .core import WeakedReference
from .dataformat import Document, Element, Path
from .decorator import classproperty, overridemethod
from .ecs import System
from .ecs import Component, Component
from .ecs import Entity, Entity
from .environment import Environment, ExitCodeType, Path, PlatformType
from .exception import SingletonError
from .filesystem import Entry, Directory, Drive, File, Storage
# from .future import EventNode, Node
# from .generic import *
from .http import HTTPStatusError
from .management import BaseManager, BaseRepository, Repository, SharedClass, Singleton
from .task import Target, Task, TaskRunner
from .utility import Filter, FileFilter, Logger, LogLevel, JSONUtility, StringUtility