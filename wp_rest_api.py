import base64
import requests
from requests.auth import HTTPBasicAuth

import settings

API_PREFIX = "wp"
API_VERSION = "v2"


class WpRESTApi:
    def __init__(self, logger, url, username, password):
        self.logger = logger
        self.url = url + "/wp-json"
        self.session = requests.Session()
        self.session.headers['user-agent'] = settings.USER_AGENT

        credentials = username + ':' + password
        self.session.headers['Authorization'] = 'Basic ' + str(base64.b64encode(credentials.encode()), 'utf-8')

    def create_post(self, **kwargs):
        resp = self.session.post(self._api_prefix('posts'), json=kwargs)
        resp.raise_for_status()
        return resp.json()

    def list_posts(self, **kwargs):
        resp = self.session.get(self._api_prefix('posts'), json=kwargs)
        resp.raise_for_status()
        return resp.json()

    def _api_prefix(self, path):
        return "/".join([self.url, API_PREFIX, API_VERSION, path])


