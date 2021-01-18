import json
import os
from typing import List


def parameterize_list(list_parameter: List[str]) -> str:
    return json.dumps(list_parameter).replace(' ', '')


def env_or_dict(dictionary: dict, key: str, find_or_failed: bool = True):
    value = os.getenv(key) or dictionary.get(key)
    if not value and find_or_failed:
        raise ValueError(key)
    return value
