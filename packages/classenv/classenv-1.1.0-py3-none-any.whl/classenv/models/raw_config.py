from classenv.models import BaseConfig
from classenv.types import VarType


class RawConfig(BaseConfig):
    def _parse(self, varname: str, varvalue: str, vartype: VarType) -> VarType:
        return str(varvalue)
