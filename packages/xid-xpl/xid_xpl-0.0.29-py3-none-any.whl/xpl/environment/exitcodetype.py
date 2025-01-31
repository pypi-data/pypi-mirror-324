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
# 전역 상수 목록.
SIGNAL: int = 128


#--------------------------------------------------------------------------------
# 종료 코드 타입.
# - 유닉스계열에서는 0~255의 정수로 제한 + 128 이후부터는 시그널 번호.
# - 시그널 번호는 운영체제나 프로세스가 특정 조건 혹은 이벤트를 알리기 위해 현재 프로세스에 보내는 메시지 번호.
# - 시그널은 import signal 후 signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0)) 방식으로 사용됨.
#--------------------------------------------------------------------------------
class ExitCodeType(Enum):
	SUCCESS = 0					# 종료 성공.
	GENERAL_ERROR = 1			# 일반적 오류.
	MISUSE_OF_BUILTINS = 2		# 명령어가 잘못 됨.
	PERMISSION_DENIED = 3		# 권한 없음으로 인한 오류.
	FILE_NOT_FOUND = 4			# 파일을 찾을 수 없음.
	OUT_OF_MEMORY = 5			# 메모리 부족.
	TIMEOUT = 124				# 시간 초과.
	CANNOT_EXECUTE = 126		# 실행 할 수 없음.
	COMMAND_NOT_FOUND = 127		# 명령어를 찾을 수 없음.
	INVALID_EXIT_ARGUMENT = 128	# 종료 코드에 잘못된 인자 전달.
	SIGHUP = SIGNAL + 1			# SIGHUP 신호로 종료. (터미널 연결이 끊어짐, 터미널이 닫힘, 데몬 프로세스의 설정 파일 재로딩)
	SIGINT = SIGNAL + 2			# SIGHUP 신호로 종료. (인터럽트 신호: CTRL+C 입력)
	SIGQUIT = SIGNAL + 3 		# SIGQUIT 신호로 종료. (종료 신호: CTRL+\ 입력)
	SIGILL = SIGNAL + 4			# SIGILL 신호로 종료. (잘못된 명령어) 
	SIGABRT = SIGNAL + 6		# SIGABRT 신호로 종료. (프로세스 중단 요청) (abort() 함수로 강제 종료로 인해 발생)
	SIGFPE = SIGNAL + 8			# SIGFPE 신호로 종료. (수학적 오류) (0으로 나누는 등)
	SIGKILL = SIGNAL + 9		# SIGKILL 신호로 종료. (강제 종료) (강제 종료 될 때 발생하는 신호) (무시 불가능한 절대 신호)
	SIGTERM = SIGNAL + 15		# SIGTERM 신호. (종료 요청) (종료 요청 신호)
	SIGSTOP = SIGNAL + 19		# SIGSTOP 신호. (프로세스 일시정지)
	SIGCONT = SIGNAL + 18		# SIGCONT 신호. (프로세스 재개)
	SIGALRM = SIGNAL + 14		# SIGALRM 신호. (일정 시간 이후 발생) (alarm() 함수로 설정한 시간이 지나면 알림)
	SIGCHLD = SIGNAL + 17		# SIGCHLD  신호. (자식 프로세스 종료시 부모 프로세스에 발생)
	SIGSEGV = SIGNAL + 11		# SIGSEGV 신호로 종료. (세그먼트 오류) (프로세스가 허용되지 않은 메모리 영역에 접근하려고 할 때 발생)
	UNKNOWN_ERROR = 255			# 알 수 없는 오류.