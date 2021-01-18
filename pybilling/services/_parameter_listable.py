from abc import ABC
from typing import List

from pybilling.utils import parameterize_list
from pybilling.constants import (ASC, DESC, DEFAULT_SORT)
from ._segregation import Listable


class ParameterListable(Listable, ABC):
    def list(self, embedded: List[str] = None,
             limit: int = 25, page: int = 1, sort: str = None, ascending: bool = False,
             filter_str: str = None, *args, **kwargs) -> list:

        if embedded:
            self._add_parameter('embedded', parameterize_list(embedded))

        if isinstance(filter_str, str):
            self._add_parameter('filters', filter_str)

        if not sort:
            sort = DEFAULT_SORT
        order = ASC if ascending else DESC
        sort = order + sort

        self._add_parameter('sort', sort)
        self._add_parameter('limit', limit)
        self._add_parameter('page', page)

        return super(ParameterListable, self).list(*args, **kwargs)
