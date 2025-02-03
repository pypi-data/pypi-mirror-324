#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import os
from xpl import Console, BaseManager


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
UTF8: str = "utf-8"
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"


#--------------------------------------------------------------------------------
# 빌드 매니저.
# - EXE, MSI, 등의 빌드 처리.
#--------------------------------------------------------------------------------
class BuildManager(BaseManager):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 빌드.
	#--------------------------------------------------------------------------------
	def Build(thisInstance, projectDirectory: str) -> bool:
		if not os.path.isdir(projectDirectory):
			return False

		# 1. 버전 파일 생성 or 갱신.
		# 2. 의존성 파일 생성 or 갱신.
		# 3. 
		return True