from urllib.parse import urljoin

import requests


class CkanAPIClient:

    def __init__(self, ckan_api_url, ckan_api_key):
        self.ckan_api_url = ckan_api_url
        self.ckan_api_key = ckan_api_key

    def get_all_datasets(self):
        packages = self.package_list()
        return (self.package_show(p) for p in packages)

    def package_list(self):
        json_response = self._send_get_request('/package_list')
        return json_response.get('result')

    def package_show(self, pkg_name):
        json_response = self._send_get_request('/package_show?',
                                                params={'id': pkg_name})
        return json_response.get('result')

    def create_url(self, suffix):
        url = urljoin(self.ckan_api_url, suffix)
        return url

    def _send_get_request(self, path, params=None):
            urlpath = self.create_url(path)
            response = requests.get(urlpath, params=params,
                                    headers={'Authorization': self.ckan_api_key})
            return response.json()
