#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from xpl import BaseRepository


#--------------------------------------------------------------------------------
# 실제 매니저의 인스턴스 저장소.
#--------------------------------------------------------------------------------
class Repository(BaseRepository):
	pass