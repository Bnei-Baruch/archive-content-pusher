import requests
import settings

JWT_ENTRY_POINT = "jwt-auth/v1/token"
API_PREFIX = "wp"
API_VERSION = "v2"


class WpRESTApi:
    def __init__(self, logger, url, username, password):
        self.logger = logger
        self.url = url + "/wp-json"
        self.session = requests.Session()
        self.session.headers['user-agent'] = settings.USER_AGENT

        resp = self.session.post(self._jwt_prefix(''),
                                 {'username': username, 'password': password})
        resp.raise_for_status()
        self.session.headers['Authorization'] = 'Bearer {}'.format(resp.json()['token'])

    def validate_token(self):
        resp = self.session.post(self._jwt_prefix('validate'))
        resp.raise_for_status()
        return resp.json()

    def create_post(self, **kwargs):
        resp = self.session.post(self._api_prefix('posts'), data=kwargs)
        resp.raise_for_status()
        return resp.json()

    def list_posts(self, **kwargs):
        resp = self.session.get(self._api_prefix('posts'), params=kwargs)
        resp.raise_for_status()
        return resp.json()

    def _api_prefix(self, path):
        return "/".join([self.url, API_PREFIX, API_VERSION, path])

    def _jwt_prefix(self, path):
        return "/".join([self.url, JWT_ENTRY_POINT, path])


