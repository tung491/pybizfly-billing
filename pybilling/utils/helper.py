import json
import os
from typing import List
import datetime
from pybilling.constants import ISO_8601


def parameterize_list(list_parameter: List[str]) -> str:
    return json.dumps(list_parameter).replace(' ', '')


def env_or_dict(dictionary: dict, key: str, find_or_failed: bool = True):
    value = os.getenv(key) or dictionary.get(key)
    if not value and find_or_failed:
        raise ValueError(key)
    return value


def locals_except(haystack: dict, excepted: list = None):
    excepted = excepted or []
    excepted.extend(['self', '__class__', 'args', 'kwargs'])
    for name in excepted:
        haystack.pop(name, None)
    return haystack


def stringfy_time(time: datetime.datetime):
    return time.strftime(ISO_8601)
