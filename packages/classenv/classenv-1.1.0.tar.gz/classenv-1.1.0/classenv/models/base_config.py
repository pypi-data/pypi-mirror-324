import abc
import os
from typing import Any, Type

from classenv.types import VarType, T, ParserCallback


class BaseConfig(metaclass=abc.ABCMeta):
    def __init__(
        self,
        klass: Type[T],
        *,
        prefix: str = "",
        delimiter: str = ",",
        parsers: dict[type, ParserCallback] = None,
        **kwargs,
    ):
        self.__annotations__ = klass.__annotations__
        self.__doc__ = klass.__doc__
        self._delimiter = delimiter
        self._prefix = prefix
        self._parsers = parsers or {}
        self._klass = klass
        self._as_dict = {}
        self.init()

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if not name.startswith("_"):
            self._as_dict[name] = value

    def init(self):
        for varname, vartype in self._klass.__annotations__.items():
            if varname.startswith("_"):
                continue
            envname = varname
            if self._prefix:
                envname = f"{self._prefix}_{envname}"
            envname = envname.upper()
            default = getattr(self._klass, varname, None)
            varvalue = os.getenv(envname, default)
            if self._is_collection(vartype, (set, frozenset, list, tuple)) and varvalue is None:
                varvalue = ""
            if self._is_collection(vartype, (dict,)) and varvalue is None:
                varvalue = dict()
            if varvalue is None:
                raise ValueError(
                    f"{envname} is a required environment variable, no default value provided."
                )
            setattr(self, varname, self._parse(varname, varvalue, vartype))

    def _is_collection(self, vartype: VarType, collection_types: tuple[type] | None = None) -> bool:
        if collection_types is None:
            collection_types = (
                list,
                tuple,
                set,
                frozenset,
                dict,
            )
        if hasattr(vartype, "__origin__") and vartype.__origin__ in collection_types:
            return True
        if vartype in collection_types:
            return True
        return False

    @abc.abstractmethod
    def _parse(self, varname: str, varvalue: str, vartype: VarType) -> VarType:
        raise NotImplementedError()  # pragma: no cover
