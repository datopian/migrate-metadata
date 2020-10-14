import requests
from requests.exceptions import RequestException
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
        response = self._send_get_request(url)
        return self.get_result(response)

    def package_show(self, pkg_name):
        params = {'id': pkg_name}
        url = self.create_url('/api/3/action/package_show', params=params)
        response = self._send_get_request(url)
        return self.get_result(response)

    def package_search(self, params=None):
        url = self.create_url('/api/3/action/package_search', params=params)
        response = self._send_get_request(url)
        return self.get_result(response)

    def get_datasets_list_from_search(self, params):
        """Iterates through the package_search API and returns a python list
        of all datasets.

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

    def get_result(self, response):
        """Get the result of the function called from the response object.

        CKAN API aims to always return 200 OK as the status code of its HTTP
        response and the actual result f the function called in the result
        element of the response.

        https://docs.ckan.org/en/2.8/api/index.html#making-an-api-request
        """
        if not response.get('success'):
            raise CkanAPIError(response.get('error')['message'])

        return response.get('result')

    def _send_get_request(self, url):
        try:
            response = requests.get(
                url, headers={'Authorization': self.ckan_api_key}
                )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise CkanAPIError(e)

        return response.json()
