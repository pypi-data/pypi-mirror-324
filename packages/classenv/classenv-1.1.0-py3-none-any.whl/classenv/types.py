from typing import (
    Callable,
    NewType,
    TypeVar,
    TypeAlias,
    Union,
)


T = TypeVar("T")
VarType = TypeVar("VarType")
ParserCallback: TypeAlias = Callable[[str, str, VarType], VarType]
Base64 = NewType("base64", bytes)
Base85 = NewType("base85", bytes)

# JSON type def
JSONLiteral = Union[None, bool, int, float, str]
JSONLiteralArray = list[JSONLiteral]
JSONLiteralDict = dict[str, Union[JSONLiteral, JSONLiteralArray]]
JSONArray = list[Union[JSONLiteral, JSONLiteralDict]]
JSONDict = dict[str, Union[JSONLiteral, JSONArray]]
JSON = Union[JSONLiteral, JSONArray, JSONDict]
