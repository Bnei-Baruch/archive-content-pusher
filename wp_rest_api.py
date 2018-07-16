import os

import requests
from requests import HTTPError


HOST_URL = os.getenv("HOST_URL", "http://blogd2.kbb1.com")
API_HOST_URL = HOST_URL + "/wp-json"
JWT_ENTRY_POINT = "jwt-auth/v1/token"
API_PREFIX = "wp"
API_VERSION = "v2"
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


class WpRESTApi:
    def __init__(self, logger, url):
        self.logger = logger
        self.url = url
        self.auth_token = None

        res = requests.post("/".join([API_HOST_URL, JWT_ENTRY_POINT]),
                            {'username': USERNAME, 'password': PASSWORD})
        res.raise_for_status()
        self.auth_token = res.json()['token']
        self.logger.info("JWT response: {}".format(res.json()))

    def validate_token(self):
        res = requests.post("/".join([API_HOST_URL, JWT_ENTRY_POINT, 'validate']),
                            headers={
                                'Authorization': 'Bearer {}'.format(self.auth_token),
                            })
        self.logger.info("Response: {}".format(res.json()))
        res.raise_for_status()

    def create_post(self, **kwargs):
        res = requests.post("/".join([API_HOST_URL, API_PREFIX, API_VERSION, 'posts']),
                            headers={
                                'Authorization': 'Bearer {}'.format(self.auth_token),
                            },
                            data=kwargs)
        try:
            res.raise_for_status()
        except HTTPError as http_err:
            self.logger.error("Error: {}".format(http_err))
            self.logger.info("Response: {}".format(res.json()))
            self.logger.info("Headers: {}".format(res.headers))
