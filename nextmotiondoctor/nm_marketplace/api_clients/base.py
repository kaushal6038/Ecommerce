import requests
from django.conf import settings


class BaseApi(object):
    token = ''

    def __init__(self, base_url):
        self.base_url = base_url

    def get_token(self):

        if self.token:
            return

        login_cred = {
            'email': settings.NEXTMOTION_MARKETPLACE_API_USER,
            'password': settings.NEXTMOTION_MARKETPLACE_API_PASSWORD
        }
        response = requests.post('%s/user/login/' % self.base_url, data=login_cred)
        api_response = response.json()
        if api_response:
            self.token = api_response['access']

    def get(self, url):
        self.get_token()
        auth_header = {'Authorization': 'Bearer {}'.format(self.token)}
        response = requests.get('%s/%s' % (self.base_url, url), headers=auth_header)
        return response.json()

    def post(self,url, **params):
        response = requests.post('%s/%s' % (self.base_url, url), json=params)
        return response.json()

    def get_product(self,url,token):
        params = {'token':token}
        response = requests.get('%s/%s' % (self.base_url, url),params=params)
        return response.json()

    def get_filter_product(self, url, **params):
        response = requests.get('%s/%s' % (self.base_url, url),params=params)
        return response.json()
