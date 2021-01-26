from typing import List

from pybilling.commons import Embeddable
from pybilling.constants import PLAN_RESOURCE_ENDPOINT
from ._parameter_gettable import ParameterGettable
from ._parameter_listable import ParameterListable
from ._parameter_patchable import ParameterPatchable
from ._segregation import (Creatable, Deletable)


class Plan(ParameterGettable, ParameterListable, Creatable, ParameterPatchable, Deletable, Embeddable):
    def _create_endpoint(self) -> str:
        return PLAN_RESOURCE_ENDPOINT

    def get(self, _id: str, embedded: List[str] = None, *args, **kwargs) -> dict:
        if not kwargs.get('auth_required'):
            kwargs['auth_required'] = False

        return super(Plan, self).get(_id, embedded, *args, **kwargs)

    def list(self, embedded: List[str] = None,
             limit: int = 25, page: int = 1, sort: str = None, ascending: bool = False,
             filter_str: str = None, *args, **kwargs) -> list:
        if not kwargs.get('auth_required'):
            kwargs['auth_required'] = False

        return super(Plan, self).list(embedded, limit, page, sort, ascending, filter_str, *args, **kwargs)

    def embeddable(self) -> List[str]:
        return ['billing_model', 'pricing_model', 'unit_prices', 'product']
