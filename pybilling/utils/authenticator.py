from pybilling.constants import (CREATE,
                                 OPENSTACK_AUTH_URL, OPENSTACK_DEFAULT_USER_DOMAIN_NAME,
                                 OPENSTACK_DEFAULT_PROJECT_DOMAIN_NAME, KEYSTONE_AUTH_PLUGIN)
from .exceptions import (AuthenticationException, BizFlyClientException)
from .helper import env_or_dict
from .https import HttpRequest
from .log import log


class Authenticator(object):
    def __init__(self, openstack_credential: dict = None):

        if not openstack_credential:
            openstack_credential = {}
        self._config = openstack_credential

        self.request_status = None
        self.new_token_arrived = False

    def request(self) -> str:
        try:
            auth_url = env_or_dict(self._config, 'OPENSTACK_AUTH_URL', False) or OPENSTACK_AUTH_URL

            username = env_or_dict(self._config, 'KEYSTONE_USER_ADMIN')
            password = env_or_dict(self._config, 'KEYSTONE_PASSWORD_ADMIN')
            user_domain_name = env_or_dict(
                self._config, 'OPENSTACK_DEFAULT_USER_DOMAIN_NAME', False
            ) or OPENSTACK_DEFAULT_USER_DOMAIN_NAME

            project_name = env_or_dict(self._config, 'KEYSTONE_TENANT_ADMIN') or username
            project_domain_name = env_or_dict(
                self._config, 'OPENSTACK_DEFAULT_PROJECT_DOMAIN_NAME', False
            ) or OPENSTACK_DEFAULT_PROJECT_DOMAIN_NAME
            method = env_or_dict(self._config, 'KEYSTONE_AUTH_PLUGIN', False) or KEYSTONE_AUTH_PLUGIN

        except ValueError as e:
            log.error('Authenticated config error. Insert access token or set up authenticated config values.')
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
