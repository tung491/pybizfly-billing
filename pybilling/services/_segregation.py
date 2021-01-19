from abc import ABC, abstractmethod

from pybilling.constants import (GET, CREATE, UPDATE, DELETE, PUT, METHODS, BILLING_API_URL)
from pybilling.utils import (build_uri, env_or_dict, HttpRequest, Authenticator, AuthenticationException)
from typing import (List, Tuple, Any)


class Service(ABC):
    def __init__(self, tenant_id: str = None, api_url: str = None, auth_token: str = None, client=None):
        self.response_content = {}
        self.response_code = None

        # for update auth token
        self.__client = client
        self.__authenticator = None
        self.__prepare_service()

        self._request_method: str = GET
        self._request_body: dict = {}
        self.__sub_endpoints: List[str] = []
        self.__parameters: List[Tuple[str, Any]] = []

        self.__tenant_id: str = tenant_id
        self.__auth_token: str = auth_token
        self.__billing_api_url: str = api_url or env_or_dict({}, 'BILLING_API_URL', False) or BILLING_API_URL

    @abstractmethod
    def _create_endpoint(self) -> str:
        pass

    def set_auth_token(self, auth_token: str):
        self.__auth_token = auth_token

    def _execute(self, method: str = None, auth_required: bool = True):
        url = self.__build_uri()
        headers = self._create_headers(auth_required)

        if method and method in METHODS:
            self._request_method = method

        # request 5 times maximum to server
        http_request = HttpRequest(method=self._request_method, url=url, headers=headers, body=self._request_body)
        self.response_code, self.response_content, _ = http_request.execute(5)

        # If token expires, request a new one and send request again.
        if self.response_code == 401 and isinstance(self.__authenticator, Authenticator):
            self.__auth_token = self.__authenticator.request()
            # trigger client update token
            self.__client.update_token()

            headers = self._create_headers(auth_required)
            self.response_code, self.response_content, _ = http_request.execute(5, headers=headers)

        # flush request data
        self.__flush_request_data()

        return self.response_content

    def _add_sub_endpoint(self, sub_endpoint: str):
        self.__sub_endpoints.append(sub_endpoint)

    def _add_parameter(self, key: str, value):
        self.__parameters.append({key: value})

    def _create_headers(self, auth_required):
        headers = {
            'Content-Type': 'application/json'
        }
        if auth_required:
            if not self.__auth_token:
                raise AuthenticationException('Auth required without authenticated token.')
            headers.update(
                {
                    'X-Auth-Token': self.__auth_token,
                    'X-Tenant-Id': self.__tenant_id,
                }
            )
        return headers

    def __build_uri(self):
        base_uri = '%s/%s' % (self.__billing_api_url, self._create_endpoint())
        return build_uri(base_uri, sub_endpoints=self.__sub_endpoints, parameters=self.__parameters)

    def __flush_request_data(self) -> bool:
        self._request_body = {}
        self.__sub_endpoints = []
        self.__parameters = []
        return True

    def __prepare_service(self):
        pass


# Interface segregation
class Gettable(Service, ABC):
    def get(self, _id: str, *args, **kwargs) -> dict:
        self._add_sub_endpoint(_id)
        auth_required = kwargs.get('auth_required', True)
        return self._execute(GET, auth_required=auth_required)


class Creatable(Service, ABC):
    def create(self, *args, **kwargs) -> dict:
        auth_required = kwargs.get('auth_required', True)
        return self._execute(CREATE, auth_required=auth_required)


class Patchable(Service, ABC):
    def update(self, *args, **kwargs) -> dict:
        auth_required = kwargs.get('auth_required', True)
        return self._execute(UPDATE, auth_required=auth_required)


class Listable(Service, ABC):
    def list(self, *args, **kwargs) -> list:
        auth_required = kwargs.get('auth_required', True)
        return self._execute(GET, auth_required=auth_required)


class Puttable(Service, ABC):
    def put(self, _id: str, *args, **kwargs) -> dict:
        self._add_sub_endpoint(_id)
        auth_required = kwargs.get('auth_required', True)
        return self._execute(PUT, auth_required=auth_required)


class Deletable(Service, ABC):
    def delete(self, _id: str, *args, **kwargs) -> dict:
        self._add_sub_endpoint(_id)
        auth_required = kwargs.get('auth_required', True)
        return self._execute(DELETE, auth_required=auth_required)
