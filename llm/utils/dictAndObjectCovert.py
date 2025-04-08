import datetime
import decimal
import uuid
from typing import Any, Dict, List, Union, Optional

class DictToObject:
    # 將字典轉換為可以使用點符號訪問的對象。
    def __init__(self, dictionary: Dict[str, Any]):
        # 遍歷字典並將每個鍵值對設為對象的屬性
        for key, value in dictionary.items():
            # 轉換值（可能是巢狀結構）
            converted_value = self._convert_value(value)
            setattr(self, key, converted_value)

    def _convert_value(self, value: Any) -> Any:
        # 轉換值，處理各種資料類型。
        # 如果值是字典，則遞歸轉換為對象
        if isinstance(value, dict):
            return DictToObject(value)
        # 如果值是列表，檢查列表中的每個元素
        elif isinstance(value, list):
            return [self._convert_value(item) for item in value]
        # 特殊類型處理 - 保持原始類型
        elif isinstance(value, (datetime.datetime, datetime.date, datetime.time,
                            decimal.Decimal, uuid.UUID, bytes, set, frozenset,
                            complex)):
            return value
        # ISO 格式日期字符串檢測與轉換
        elif isinstance(value, str):
            # 嘗試解析 ISO 格式的日期時間字符串
            try:
                if 'T' in value and ('+' in value or 'Z' in value):
                    # 可能是 ISO 格式的日期時間
                    return datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
                elif '-' in value and len(value) == 10 and value.count('-') == 2:
                    # 可能是日期 YYYY-MM-DD
                    return datetime.date.fromisoformat(value)
            except ValueError:
                # 如果解析失敗，保持原始字符串
                pass
        # 其他所有類型保持不變
        return value

def dict_to_object(dictionary: Union[Dict[str, Any], Any]) -> Any:
    """將字典轉換為對象。
    Args:
        dictionary: 要轉換的字典或其他值
    Returns:
        轉換後的對象或原始值
    """
    if not isinstance(dictionary, dict):
        return dictionary
    return DictToObject(dictionary)

def object_to_dict(obj: Any) -> Any:
    """將對象轉換為字典。
    Args:
        obj: 要轉換的對象
    Returns:
        轉換後的字典或值
    """
    # 處理特殊類型
    if obj is None:
        return None
    # 處理日期時間類型
    elif isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    # 處理 Decimal
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    # 處理 UUID
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    # 處理 bytes
    elif isinstance(obj, bytes):
        try:
            return obj.decode('utf-8')
        except UnicodeDecodeError:
            return str(obj)
    # 處理 set/frozenset
    elif isinstance(obj, (set, frozenset)):
        return list(obj)
    # 處理複數
    elif isinstance(obj, complex):
        return {"real": obj.real, "imag": obj.imag}
    # 處理字典
    elif isinstance(obj, dict):
        return {k: object_to_dict(v) for k, v in obj.items()}
    # 處理列表和元組
    elif isinstance(obj, (list, tuple)):
        return [object_to_dict(item) for item in obj]
    # 處理有 __dict__ 屬性的對象
    elif hasattr(obj, "__dict__"):
        result = {}
        for key, value in obj.__dict__.items():
            # 跳過以下劃線開頭的私有屬性
            if key.startswith("_"):
                continue
            result[key] = object_to_dict(value)
        return result
    # 其他原始類型保持不變
    return obj