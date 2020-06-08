import pytest
from mock import patch
from migrate_metedata import migrator
import metastore.backend as metastore
from Ckan_API.Ckan_API import CkanAPICall


@patch('migrator.CkanAPICall.get_all_datasets')
def test_migrate_all_datasets(mock_get_all_datasets):
    mock_reutrn_value = {'result': [{0: {
                    "name": "test_pkg_0"}},
                    {1: {
                    "name": "test_pkg_1"}}
                    ]}
    mock_get_all_datasets.return_value = mock_reutrn_value
    ckan_client = CkanAPICall("http://test", "xyz-123")

    metastore_client = metastore.create_metastore("filesystem", dict(uri="mem://"))
    number_of_datasets = migrator.migrate_all_datasets(ckan_client, metastore_client)

    assert len(mock_reutrn_value) == number_of_datasets
