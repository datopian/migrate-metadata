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

    def package_search(self, params=None):
        url = self.create_url('/api/3/action/package_search', params=params)
        response = requests.get(
            url, headers={'Authorization': self.ckan_api_key}
            )
        data = response.json()
        return self.get_result(data)

    def get_datasets_list_from_search(self, params):
        """Iterates through the package_search API and returns a python list
        of all datasets including draft and private ones.

        In order to extract a clean complete list of datasets objects we need to
        iterate over the hard limit of 1000 per query and on each extract the
        dataset list from the result json.
        """
        datasets = []
        start = 0
        while True:
            params['start'] = start
            result = self.package_search(params=params)
            rows = result['results']
            if rows == []:
                break
            datasets.extend(rows)
            start += len(rows)

        return datasets

    def create_url(self, path, params=None):
        url = urljoin(self.ckan_api_url, path)
        if params:
            url += '?' + urlencode(params)
        return url

    def get_result(self, data):
        if not data.get('success'):
            raise CkanAPIError(data.get('error')['message'])

        return data.get('result')
