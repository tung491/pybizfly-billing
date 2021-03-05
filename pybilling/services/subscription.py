import datetime

from pybilling.constants import (SUBSCRIPTION_RESOURCE_ENDPOINT,
                                 HANOI_REGION,
                                 SUBSCRIBE_ACTION, UPDATE_ACTION, RENEW_ACTION, CLOSE_ACTION,
                                 DEFAULT_CATEGORY_CODE)
from pybilling.utils import stringfy_time, List
from ._parameter_gettable import ParameterGettable
from ._parameter_listable import ParameterListable
from ._segregation import (Creatable, Patchable)
from .billing_model import Embeddable


class Subscription(ParameterGettable, ParameterListable, Creatable, Patchable, Embeddable):
    def _create_endpoint(self) -> str:
        return SUBSCRIPTION_RESOURCE_ENDPOINT

    def subscribe(self, plan_name: str,
                  resource_name: str, resource_ref: str, related_ref: str = None,
                  quantity: float = 0, executed_at: datetime.datetime = None,
                  region_name: str = None, category_code: str = None,
                  many: list = None, *args, **kwargs) -> list:

        action = SUBSCRIBE_ACTION
        if many:
            for item in many:
                item['action'] = SUBSCRIBE_ACTION

        return self.create(plan_name, resource_name, resource_ref, action,
                           quantity=quantity, executed_at=executed_at, region_name=region_name,
                           related_ref=related_ref, category_code=category_code, many=many, *args, **kwargs)

    def log(self, plan_name: str,
            resource_name: str, resource_ref: str,
            quantity: int = 0, executed_at: datetime.datetime = None,
            region_name: str = None, category_code: str = None,
            many: list = None, *args, **kwargs) -> list:

        action = UPDATE_ACTION
        if many:
            for item in many:
                item['action'] = UPDATE_ACTION

        return self.create(plan_name, resource_name, resource_ref, action,
                           quantity=quantity, executed_at=executed_at, region_name=region_name,
                           category_code=category_code, many=many, *args, **kwargs)

    def renew(self, plan_name: str,
              resource_name: str, resource_ref: str,
              quantity: int = 0, executed_at: datetime.datetime = None,
              region_name: str = None, category_code: str = None,
              many: list = None, *args, **kwargs) -> list:

        action = RENEW_ACTION
        if many:
            for item in many:
                item['action'] = RENEW_ACTION

        return self.create(plan_name, resource_name, resource_ref, action,
                           quantity=quantity, executed_at=executed_at, region_name=region_name,
                           category_code=category_code, many=many, *args, **kwargs)

    def close(self, plan_name: str,
              resource_name: str, resource_ref: str,
              quantity: int = 0, executed_at: datetime.datetime = None,
              region_name: str = None, category_code: str = None,
              many: list = None, *args, **kwargs) -> list:

        action = CLOSE_ACTION
        if many:
            for item in many:
                item['action'] = CLOSE_ACTION

        return self.create(plan_name, resource_name, resource_ref, action,
                           quantity=quantity, executed_at=executed_at, region_name=region_name,
                           category_code=category_code, many=many, *args, **kwargs)

    def create(self, plan_name: str,
               resource_name: str, resource_ref: str, action: str,
               quantity: int, executed_at: datetime.datetime,
               region_name: str, category_code: str, related_ref: str = "",
               many: list = None, *args, **kwargs) -> list:
        many = many or []

        quantity = quantity or 0
        executed_at = executed_at or datetime.datetime.utcnow()
        region_name = region_name or HANOI_REGION
        category_code = category_code or DEFAULT_CATEGORY_CODE

        self._request_body = [
            {
                'plan_name': plan_name,
                'resource_name': resource_name,
                'resource_ref': resource_ref,
                'related_ref': related_ref,
                'quantity': quantity,
                'action': action,
                'executed_at': stringfy_time(executed_at),
                'region_name': region_name,
                'category_code': category_code
            },
            *many
        ]

        return super(Subscription, self).create(*args, **kwargs)

    def switch_plan(self, plan_name: str, resource_name: str, resource_ref: str,
                    switchable_plan_name: str,
                    switchable_resource_name: str = None, switchable_resource_ref: str = None,
                    region_name: str = HANOI_REGION, executed_at: datetime = datetime.datetime.utcnow(),
                    many: list = None, *args, **kwargs) -> list:
        many = many or []
        item = {
            'plan_name': plan_name,
            'resource_name': resource_name,
            'resource_ref': resource_ref,
            'switchable_plan_name': switchable_plan_name,
            'executed_at': stringfy_time(executed_at),
            'region_name': region_name,
        }

        if switchable_resource_name:
            item['switchable_resource_name'] = switchable_resource_name
        if switchable_resource_ref:
            item['switchable_resource_ref'] = switchable_resource_ref

        self._request_body = [item, *many]
        self._add_sub_endpoint('switch')
        return super(Subscription, self).update(*args, **kwargs)

    def upgrade_trial(self, plan_name: str, resource_name: str, resource_ref: str,
                      switchable_resource_name: str = None, switchable_resource_ref: str = None,
                      region_name: str = HANOI_REGION, executed_at: datetime = datetime.datetime.utcnow(),
                      many: list = None, *args, **kwargs) -> dict:
        many = many or []
        item = {
            'plan_name': plan_name,
            'resource_name': resource_name,
            'resource_ref': resource_ref,
            'executed_at': stringfy_time(executed_at),
            'region_name': region_name,
        }

        if switchable_resource_name:
            item['switchable_resource_name'] = switchable_resource_name
        if switchable_resource_ref:
            item['switchable_resource_ref'] = switchable_resource_ref

        self._request_body = [item, *many]
        self._add_sub_endpoint('upgrade')
        return super(Subscription, self).update(*args, **kwargs)

    def embeddable(self) -> List[str]:
        return ['plan', 'account', 'usages']

    def unsubscribe(self, resource_ref: str,
                    region_name: str = HANOI_REGION, executed_at: datetime = datetime.datetime.utcnow(),
                    many: list = None, *args, **kwargs) -> list:
        many = many or []
        item = {
            'resource_ref': resource_ref,
            'executed_at': stringfy_time(executed_at),
            'region_name': region_name,
        }

        self._request_body = [item, *many]
        self._add_sub_endpoint('unsubscribe')
        return super(Subscription, self).create(*args, **kwargs)

    def update_related_ref(self, id_: str, related_ref: str, many: list = None, *args, **kwargs):
        many = many or []
        items = [{
            'id': id_,
            'related_ref': related_ref,
        }, *many]
        self._request_body = items
        return super(Subscription, self).update(*args, **kwargs)

