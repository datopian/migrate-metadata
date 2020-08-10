import pytest
from mock import patch
from migrate_metadata import migrator
import metastore.backend as metastore
from ckan_api.ckan_api import CkanAPIClient


@patch('migrator.CkanAPIClient.get_all_datasets')
def test_migrate_all_datasets(mock_get_all_datasets):
    mock_reutrn_value = {'result': [{0: {
                    "name": "test_pkg_0",
                    "author": "test_user"}},
                    {1: {
                    "name": "test_pkg_1",
                    "author": "test_user"}}
                    ]}
    mock_get_all_datasets.return_value = mock_reutrn_value
    ckan_client = CkanAPIClient("http://test", "xyz-123")

    metastore_client = metastore.create_metastore("filesystem", dict(uri="mem://"))
    number_of_datasets = migrator.migrate_all_datasets(ckan_client, metastore_client)

    assert len(mock_reutrn_value) == number_of_datasets
