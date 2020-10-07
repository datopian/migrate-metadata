import requests
from six.moves.urllib.parse import urlencode, urljoin


class CkanAPIError(Exception):
    pass


class CkanAPIClient:
    """Wrapper for the CKAN API
    """
    def __init__(self, ckan_api_url, ckan_api_key):
        self.ckan_api_url = ckan_api_url
        self.ckan_api_key = ckan_api_key

    def package_list(self):
        url = self.create_url('/api/3/action/package_list')
        response = requests.get(
            url, headers={'Authorization': self.ckan_api_key}
            )
        data = response.json()
        return self.get_result(data)

    def package_show(self, pkg_name):
        params = {'id': pkg_name}
        url = self.create_url('/api/3/action/package_show', params=params)
        response = requests.get(
            url, headers={'Authorization': self.ckan_api_key}
            )
        data = response.json()
        return self.get_result(data)

    def create_url(self, path, params=None):
        url = urljoin(self.ckan_api_url, path)
        if params:
            url += '?' + urlencode(params)
        return url

    def get_result(self, data):
        if not data.get('success'):
            raise CkanAPIError(data.get('error')['message'])

        return data.get('result')
