from pybilling.constants import ACCOUNT_RESOURCE_ENDPOINT
from ._parameter_gettable import ParameterGettable
from ._parameter_listable import ParameterListable


class Account(ParameterGettable, ParameterListable):
    def _create_endpoint(self) -> str:
        return ACCOUNT_RESOURCE_ENDPOINT
