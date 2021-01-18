from pybilling.constants import METHODS
from .exceptions import ExcludeValueException


def validate_str_list(str_list: list) -> list:
    """
    Validate list with string instance items

    :param str_list:
    :return:
    """
    validate_list = []
    for item in str_list:
        try:
            item = str(item)
            validate_list.append(item)
        except ValueError:
            continue
    return validate_list


def validate_dict_list(dict_list: list) -> list:
    """
    Validate list with dict  instance items

    :param dict_list:
    :return:
    """
    validate_list = [] = list()
    for item in dict_list:
        if isinstance(item, dict):
            validate_list.append(item)
    return validate_list


def validate_method(method: str):
    """
    Restrict allowed method

    :param method:
    :return:
    """
    __in_list(item=method, haystack=METHODS, name_to_call='method')


def __in_list(item, haystack: list, name_to_call: str):
    if item not in haystack:
        raise ExcludeValueException(name_to_call, haystack)


