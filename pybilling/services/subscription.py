from pybilling.constants import SUBSCRIPTION_RESOURCE_ENDPOINT
from ._parameter_gettable import ParameterGettable
from ._parameter_listable import ParameterListable
from ._segregation import (Creatable, Patchable)
import datetime


class Subscription(ParameterGettable, ParameterListable, Creatable, Patchable):
    def _create_endpoint(self) -> str:
        return SUBSCRIPTION_RESOURCE_ENDPOINT

    def create(self, plan_name: str, resource_name: str, resource_ref: str,
               quantity: int = 0, action: str = 'UPDATE', executed_at: datetime.datetime = datetime.datetime.now(),
               region_name: str = 'Hanoi', category_code: str = 'DF',
               *args, **kwargs) -> dict:
        self._request_body = {
            'plan_name': plan_name,
            'resource_name': region_name,
            'resource_ref': resource_ref,
            'quantity': quantity,
            'executed_at': executed_at,
            'region_name': region_name,
            'category_code': category_code
        }

        return super(Subscription, self).create(*args, **kwargs)
