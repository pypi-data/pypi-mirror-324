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
from abc import ABC as Interface
from abc import ABC as IInterface
from abc import ABCMeta as InterfaceMetaClass
from abc import ABCMeta as IInterfaceMetaClass
from abc import abstractmethod
from .basemetaclass import BaseMetaClass


#--------------------------------------------------------------------------------
# 결합된 인터페이스 메타 클래스.
# - 인터페이스를 상속받은 클래스는 인터페이스메타클래스를 사용하기 때문에 메타클래스의 변형을 다룰때는 다음과 같이 다룬다.
# - 이렇게 두개의 메타를 같이 받고, 아래 주석처럼 다중상속을 통해 결합된 메타클래스를 만들고 해당 내용에 로직을 구현하고 메타클래스로 사용하면 된다.
# - class INode(Interface, metaclass = CombinedInterfaceMetaClass) 이런식으로 인터페이스를 선언하는 것이다.
#--------------------------------------------------------------------------------
class CombinedInterfaceMetaClass(BaseMetaClass, InterfaceMetaClass):
	pass


#--------------------------------------------------------------------------------
# 인스턴스화를 허용하지 않는 메타 클래스.
# - 샘플 겸해서 만들어 본 인터페이스의 상속 클래스를 외부에서 함수 방식의 호출로 객체가 생성되지 않도록 해주는 인터페이스용 메타 클래스.
#--------------------------------------------------------------------------------
class NoInstantiationMetaClass (BaseMetaClass, InterfaceMetaClass):
	#--------------------------------------------------------------------------------
	# 호출 프로토콜 메서드.
	# - 이 예제는 대상 클래스 객체가 생성될 때 익셉션을 라이즈한다.
	# - 쉽게 말해 a = A() 일때, A()는 __call__ 로 들어오니 이를 막는 것이다.
	# - 직접적인 생성자 호출만 막는 것이므로 다음과 같이 a = Object.__new__(A) 를 통해 클래스를 넘겨 객체를 생성할 수 있기 때문에 어디까지나 쓰지말라는 경고 차원이다.
	# - 파이썬은 견고하지 않기 때문에 사실 필요에 따라 얼마든 멋대로 생성해 낼 수 있다.
	# - 그럼에도 불구하고 사용해야하는 이유는 명시적으로 하지 않도록 설정하는 것이 안정적인 결과물을 만들어내는데 보탬이 되기 때문이다.
	# - 주석으로 경고만 하고 문법적으로 허용해버리면 안읽어서 몰랐다고 하면 그만이다. 힘들게 막아놔야 힘들게 뚫는 코드가 올라오게 되니 상대의 의도가 보다 명확해진다. 
	#--------------------------------------------------------------------------------
	def __call__(thisClassType, *argumentList, **argumentDictionary) -> None:
		raise ValueError("This object must not be created directly via its constructor.")