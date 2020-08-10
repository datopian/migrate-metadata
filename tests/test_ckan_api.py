import pytest
import requests_mock

from migrate_metadata.ckan_api import CkanAPIClient


@pytest.fixture()
def ckan_client():
    ckan_api_obj = CkanAPIClient("http://test", "xyz-123")
    return ckan_api_obj


def test_create_url(ckan_client):
    suffix = '/method.com'
    url = "http://test{}".format(suffix)
    assert url == ckan_client.create_url(suffix)


@requests_mock.Mocker()
def test_package_show(mock_request, ckan_client):
    url = 'http://test/package_show?'
    pkg_name = "test_pkg"
    json_resp = {'result': {"package_dict": {"name": "test_pkg", "author": "test_user"}}}
    mock_request.get(url,
                     params={'id': pkg_name},
                     headers={"Authorization": "xyz-123"},
                     json=json_resp)

    resp = ckan_client.package_show(pkg_name)
    assert json_resp['result'] == resp


@requests_mock.Mocker()
def test_package_list(mock_request, ckan_client):
    url = 'http://test/package_list'
    json_resp = {'result': [{0: {"name": "test_pkg_0", "author": "test_user"}},
                            {1: {"name": "test_pkg_1", "author": "test_user"}}]}
    mock_request.get(url,
                     headers={"Authorization": "xyz-123"},
                     json=json_resp)

    resp = ckan_client.package_list()
    assert json_resp['result'] == resp
