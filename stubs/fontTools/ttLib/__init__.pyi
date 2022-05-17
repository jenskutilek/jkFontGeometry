from io import BytesIO
from typing import Optional, Union


class TTFont(object):
    def __init__(
        self,
        file: Optional[Union[str, BytesIO]] = None,
        res_name_or_index: Optional[Union[str, int]] = None,
        sfntVersion: str = "\000\001\000\000",
        flavor: Optional[str] = None,
        checkChecksums: int = 0,
        verbose=None,
        recalcBBoxes: bool = True,
        allowVID=NotImplemented,
        ignoreDecompileErrors: bool = False,
        recalcTimestamp: bool = True,
        fontNumber: int = -1,
        lazy: Optional[bool] = None,
        quiet=None,
        _tableCache=None,
        cfg: dict = {},
    ): ...
