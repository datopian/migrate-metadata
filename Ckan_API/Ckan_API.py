from urllib.parse import urljoin

import requests


class CkanAPICall:

    def __init__(self, ckan_api_url, ckan_api_key):
        self.ckan_api_url = ckan_api_url
        self.ckan_api_key = ckan_api_key

    def get_all_datasets(self):
        packages = self.package_list()

        datasets = []
        for package in packages:
            datasets.append(self.package_show(package))
        return datasets

    def package_list(self):
        urlpath = self.create_url('/package_list')
        response = requests.get(urlpath, headers=
                                {'Authorization': self.ckan_api_key})
        json_response = response.json()
        return json_response.get('result')

    def package_show(self, pkg_name):
        urlpath = self.create_url('/package_show?')

        response = requests.get(urlpath, params={'id': pkg_name},
                                headers={'Authorization': self.ckan_api_key})
        json_response = response.json()
        return json_response.get('result')

    def create_url(self, suffix):
        url = urljoin(self.ckan_api_url, suffix)
        return url
