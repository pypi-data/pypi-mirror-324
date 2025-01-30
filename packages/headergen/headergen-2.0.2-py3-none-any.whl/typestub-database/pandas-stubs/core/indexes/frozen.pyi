from pandas.core.base import PandasObject as PandasObject
from pandas.io.formats.printing import pprint_thing as pprint_thing
from typing import Union, Any

class FrozenList(PandasObject, list):
    def union(self, other) -> FrozenList: ...
    def difference(self, other) -> FrozenList: ...
    __add__: Any
    __iadd__: Any
    def __getitem__(self, n): ...
    def __radd__(self, other): ...
    def __eq__(self, other: Any) -> bool: ...
    __req__: Any
    def __mul__(self, other): ...
    __imul__: Any
    def __reduce__(self): ...
    def __hash__(self): ...
    __setitem__: Any
    __setslice__: Any
    __delitem__: Any
    __delslice__: Any
    pop: Any
    append: Any
    extend: Any
    remove: Any
    sort: Any
    insert: Any
