from ._segregation import (Creatable, Patchable, Deletable)
from ._parameter_gettable import ParameterGettable
from ._parameter_listable import ParameterListable
from pybilling.constants import PLAN_RESOURCE_ENDPOINT


class Plan(ParameterGettable, ParameterListable, Creatable, Patchable, Deletable):
    def _create_endpoint(self) -> str:
        return PLAN_RESOURCE_ENDPOINT
