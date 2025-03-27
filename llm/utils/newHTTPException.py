from typing import Any, Dict, Union
from fastapi import HTTPException

# 自定義 HTTPException
class NewHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: Any = None, headers: Union[Dict[str, Any], None] = None, msg: str = None) -> None:
        super().__init__(status_code, detail, headers)
        if msg:
            self.msg = msg
        else:
            self.msg = detail