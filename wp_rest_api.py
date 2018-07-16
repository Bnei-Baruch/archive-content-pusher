import os

import requests
from requests import HTTPError

JWT_ENTRY_POINT = "jwt-auth/v1/token"
API_PREFIX = "wp"
API_VERSION = "v2"


class WpRESTApi:
    def __init__(self, logger, url, username, password):
        self.logger = logger
        self.url = url + "/wp-json"
        self.auth_token = None

        res = requests.post("/".join([self.url, JWT_ENTRY_POINT]),
                            {'username': username, 'password': password})
        res.raise_for_status()
        self.auth_token = res.json()['token']
        self.logger.info("JWT response: {}".format(res.json()))

    def validate_token(self):
        res = requests.post("/".join([self.url, JWT_ENTRY_POINT, 'validate']),
                            headers={
                                'Authorization': 'Bearer {}'.format(self.auth_token),
                            })
        self.logger.info("Response: {}".format(res.json()))
        res.raise_for_status()

    def create_post(self, **kwargs):
        res = requests.post("/".join([self.url, API_PREFIX, API_VERSION, 'posts']),
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

    def list_posts(self, params, **kwargs):
        res = requests.get("/".join([self.url, API_PREFIX, API_VERSION, 'posts']),
                           params,
                           headers={
                               'Authorization': 'Bearer {}'.format(self.auth_token),
                           },
                           **kwargs)
        try:
            res.raise_for_status()
        except HTTPError as ex:
            self.logger.error("Error: {}".format(ex))
            self.logger.info("Response: {}".format(res.json()))
            self.logger.info("Headers: {}".format(res.headers))
            raise ex

        return res.json()
