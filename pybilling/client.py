from dotenv import load_dotenv

from pybilling.services import *
from pybilling.utils.authenticator import Authenticator


class BizFlyBillingClient(object):
    def __init__(self, tenant_id: str = None, access_token: str = None,
                 api_url: str = None, config: dict = None):
        load_dotenv()
        self.__tenant_id = tenant_id
        self.__config = config
        self.__api_url = api_url
        self.__authenticator = Authenticator(config)

        if not access_token:
            access_token = self.__authorize()
        self.__access_token = access_token

        self.subscribers = []

    def get_authenticator(self) -> Authenticator:
        return self.__authenticator

    def plan(self) -> Plan:
        return self._create_service(Plan)

    def subscription(self) -> Subscription:
        return self._create_service(Subscription)

    def _create_service(self, service_type: type(Service)) -> Service:
        service = service_type(self.__tenant_id,
                               api_url=self.__api_url, auth_token=self.__access_token, client=self)
        self.subscribers.append(service)
        return service

    def __authorize(self):
        token = self.__authenticator.request()
        self.__authenticator.reset()
        return token