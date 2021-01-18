from pybilling.constants import CREATE
from .exceptions import (AuthenticationException, BizFlyClientException)
from .helper import env_or_dict
from .https import HttpRequest


class Authenticator(object):
    def __init__(self, config: dict = None):
        if not config:
            config = {}
        self._config = config
        self.request_status = None
        self.new_token_arrived = False

    def request(self) -> str:
        try:
            auth_url = env_or_dict(self._config, 'OPENSTACK_AUTH_URL')

            project_name = env_or_dict(self._config, 'KEYSTONE_TENANT_ADMIN')
            project_domain_name = env_or_dict(self._config, 'OPENSTACK_DEFAULT_PROJECT_DOMAIN_NAME')
            method = env_or_dict(self._config, 'KEYSTONE_AUTH_PLUGIN')

            username = env_or_dict(self._config, 'KEYSTONE_USER_ADMIN')
            password = env_or_dict(self._config, 'KEYSTONE_PASSWORD_ADMIN')
            user_domain_name = env_or_dict(self._config, 'OPENSTACK_DEFAULT_USER_DOMAIN_NAME')

        except ValueError as e:
            raise BizFlyClientException('Invalid configuration for %s' % str(e))

        auth_request_body = {
            "auth": {
                "scope": {
                    "project": {
                        "name": project_name,
                        "domain": {
                            "name": project_domain_name
                        }
                    }
                },
                "identity": {
                    "methods": [
                        method
                    ],
                    "password": {
                        "user": {
                            "name": username,
                            "domain": {
                                "name": user_domain_name
                            },
                            "password": password
                        }
                    }
                }
            }
        }

        http_request = HttpRequest(auth_url, method=CREATE, body=auth_request_body,
                                   headers={'content-type': 'application/json'})
        self.request_status, _, response_headers = http_request.execute(5)

        if self.request_status == 201:
            try:
                self.new_token_arrived = True
                return response_headers['x-subject-token']
            except ValueError:
                raise BizFlyClientException('Auth service error')

        raise AuthenticationException()

    def reset(self):
        self.new_token_arrived = False
