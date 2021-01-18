from abc import ABC
from typing import List

from pybilling.utils import parameterize_list
from ._segregation import Gettable


class ParameterGettable(Gettable, ABC):
    def get(self, _id: str, embedded: List[str] = None, *args, **kwargs) -> dict:
        if embedded:
            self._add_parameter('embedded', parameterize_list(embedded))
        return super(ParameterGettable, self).get(_id, *args, **kwargs)
