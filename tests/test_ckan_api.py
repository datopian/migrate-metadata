import pytest
import requests_mock
import json

from migrate_metadata.ckan_api import CkanAPIClient, CkanAPIError


@pytest.fixture()
def ckan_client():
    ckan_api_obj = CkanAPIClient("http://ckan:5000", "xyz-123")
    return ckan_api_obj


def test_create_url(ckan_client):
    path = '/action/method'
    expected_url = "http://ckan:5000{}".format(path)
    assert expected_url == ckan_client.create_url(path)

def test_create_url_with_params(ckan_client):
    path = '/action/method'
    package_id = 'my-package-id'
    expected_url = "http://ckan:5000{}?id={}".format(path, package_id)
    params = {'id': package_id}
    assert expected_url == ckan_client.create_url(path, params=params)

def test_get_result_returns_result_element_of_response(ckan_client):
    data = json.loads('{"help": "http://ckan:5000/api/3/action/help_show?name=package_list", "success": true, "result": ["dataset-with-no-releases", "github-dataset", "new-dataset-on-github", "testing-personal-storage-account", "testing-removed-resources"]}')
    assert ckan_client.get_result(data) == data['result']

def test_get_result_raises_error_if_api_call_returns_success_false(ckan_client):
    data = json.loads('{"help": "http://ckan:5000/api/3/action/help_show?name=package_show", "success": false, "error": {"message": "Not found", "__type": "Not Found Error"}}')
    with pytest.raises(CkanAPIError) as execinfo:
        ckan_client.get_result(data)
    assert str(execinfo.value) == "Not found"

def test_package_list(requests_mock, ckan_client):
    mock_content = '{"help": "http://ckan:5000/api/3/action/help_show?name=package_list", "success": true, "result": ["dataset-with-no-releases", "github-dataset", "new-dataset-on-github", "testing-personal-storage-account", "testing-removed-resources"]}'
    mocked_url = ckan_client.create_url('/api/3/action/package_list')
    requests_mock.get(mocked_url, content=mock_content)
    assert json.loads(mock_content)['result'] == ckan_client.package_list()

def test_package_show(requests_mock, ckan_client):
    mock_content = '{"help": "http://ckan:5000/api/3/action/help_show?name=package_show", "success": true, "result": {"name": "github-dataset"} }'
    mocked_url = ckan_client.create_url('/api/3/action/package_show')
    requests_mock.get(mocked_url, content=mock_content)
    result = json.loads(mock_content)['result']

    assert result == ckan_client.package_show("github-dataset")
