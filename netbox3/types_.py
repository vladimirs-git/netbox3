"""Typing."""
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union, Sequence, TypeVar

# 1 level
DAny = Dict[str, Any]
DInt = Dict[str, int]
DObj = Dict[str, object]
DStr = Dict[str, str]
LBool = List[bool]
LInt = List[int]
LPath = List[Path]
LStr = List[str]
LTInt2 = List[Tuple[int, int]]
ODatetime = Optional[datetime]
ODict = Optional[dict]
Param = Tuple[str, Any]
SInt = Set[int]
SStr = Set[str]
SeqStr = Sequence[str]
StrInt = Union[str, int]
T = TypeVar("T")
T2Str = Tuple[str, str]
T3Str = Tuple[str, str, str]
TLists = (list, set, tuple)
TStr = Tuple[str, ...]
TValues = (str, int, float)
Value = Union[str, int, float]

# 2 level
DDAny = Dict[str, DAny]
DDStr = Dict[str, DStr]
DLInt = Dict[str, LInt]
DLStr = Dict[str, LStr]
DList = Dict[str, list]
DSStr = Dict[str, SStr]
DiDAny = Dict[int, DAny]
DiStr = Dict[int, str]
LDAny = List[DAny]
LDStr = List[DStr]
LParam = List[Param]
LT = List[T]
LT2StrDAny = List[Tuple[str, DAny]]
LTup2 = List[T2Str]
LValue = List[Value]
ODAny = Optional[DAny]
OSeqStr = Optional[SeqStr]
SParam = Set[Param]
SeqDAny = Sequence[DAny]
SeqT = Sequence[T]
T3SStr = Tuple[SStr, SStr, SStr]
TParam = Tuple[Param, ...]
UStr = Union[str, SeqStr]

# 3 level
DDDLStr = Dict[str, Dict[str, DLStr]]
DDLInt = Dict[str, DLInt]
LDList = List[DList]
LLDAny = List[LDAny]
LLParam = List[LParam]
OUStr = Optional[UStr]
ULDAny = Union[LDAny, DAny]

# 4 level
DDDLInt = Dict[str, DDLInt]
UParam = Union[LParam, SParam, TParam]

# 5 level
OUParam = Optional[UParam]
