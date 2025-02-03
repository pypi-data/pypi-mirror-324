from base64 import b64decode, b85decode
import json
import os
from pathlib import Path

from classenv.models import BaseConfig
from classenv.types import VarType, Base64, Base85, JSON


class ParsedConfig(BaseConfig):
    def _parse(self, varname: str, varvalue: str, vartype: VarType) -> VarType:
        if self._is_collection(vartype):
            return self._parse_collection(varname, varvalue, vartype)
        return self._parse_item(varname, varvalue, vartype)

    def _parse_collection(
        self, varname: str, varvalue: str, vartype: VarType
    ) -> VarType:
        origin = getattr(vartype, "__origin__", vartype)
        if origin in (list, tuple):
            return self._parse_list(varname, varvalue, vartype)
        if origin in (set, frozenset):
            return self._parse_set(varname, varvalue, vartype)
        if origin is dict:
            return self._parse_dict(varname, varvalue, vartype)

    def _parse_list(self, varname: str, varvalue: str, vartype: VarType) -> VarType:
        if not varvalue:
            return tuple()
        if hasattr(vartype, "__args__") and vartype.__args__:
            return tuple(
                self._parse_item(varname, item, vartype.__args__[0])
                for item in varvalue.split(self._delimiter)
            )
        return tuple(
            self._parse_item(varname, item, str)
            for item in varvalue.split(self._delimiter)
        )

    def _parse_set(self, varname: str, varvalue: str, vartype: VarType) -> VarType:
        if not varvalue:
            return frozenset()
        if hasattr(vartype, "__args__") and vartype.__args__:
            return frozenset(
                self._parse_item(varname, item, vartype.__args__[0])
                for item in varvalue.split(self._delimiter)
            )
        return frozenset(
            self._parse_item(varname, item, str)
            for item in varvalue.split(self._delimiter)
        )

    def _parse_dict(self, varname: str, varvalue: str, vartype: VarType) -> VarType:
        keytype, valuetype = getattr(varvalue, "__args__", (str, str))
        if self._prefix:
            envname = f"{self._prefix}_{varname}".upper()
        else:
            envname = varname.upper()
        env_variables = {k: v for k, v in os.environ.items() if k.startswith(envname)}
        return {
            self._parse_item(
                name, name.replace(envname, "").lstrip("_"), keytype
            ): self._parse_item(name, value, valuetype)
            for name, value in env_variables.items()
        }

    def _parse_item(self, varname: str, item: str, vartype: VarType) -> VarType:
        if vartype in self._parsers:
            # User-defined parsers should take precedence over everything else
            return self._parsers[vartype](varname, item, vartype)
        if vartype is str:
            return self._parse_str(varname, item)
        if vartype is int:
            return self._parse_int(varname, item)
        if vartype is float:
            return self._parse_float(varname, item)
        if vartype is bool:
            return self._parse_bool(varname, item)
        if vartype is Path:
            return Path(self._parse_str(varname, item))
        if vartype is Base64:
            return self._parse_base64(varname, item)
        if vartype is Base85:
            return self._parse_base85(varname, item)
        if vartype is JSON:
            return self._parse_json(varname, item)
        raise TypeError(f"Unsupported type {vartype} for {varname}")

    def _parse_int(self, varname: str, item: str) -> int:
        if item.startswith("0o"):
            return int(item, 8)
        if item.startswith("0x"):
            return int(item, 16)
        if item.startswith("0b"):
            return int(item, 2)
        if not item.isnumeric():
            raise ValueError(f"Invalid int value {item} for {varname}")
        return int(item)

    def _parse_bool(self, varname: str, item: str) -> bool:
        if item.lower() in ("true", "yes", "on", "y"):
            return True
        if item.isdigit() and int(item) > 0:
            return True
        return False

    def _parse_float(self, varname: str, item: str) -> float:
        return float(item)

    def _parse_str(self, varname: str, item: str) -> str:
        return str(item)

    def _parse_base64(self, varname: str, item: str) -> bytes:
        return b64decode(str(item).encode('utf-8'))

    def _parse_base85(self, varname: str, item: str) -> bytes:
        return b85decode(str(item).encode('utf-8'))

    def _parse_json(self, varname: str, item: str) -> JSON:
        return json.loads(item)

    def to_json(self) -> str:
        return json.dumps(self._as_dict, indent=2)
