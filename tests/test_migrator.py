import metastore.backend as metastore
from migrate_metadata import migrator


def test_migrate_datasets_migrates_only_of_type_dataset():
    datasets = [
        {"name": "test_pkg_0", "author": "test_user", "type": "dataset"},
        {"name": "test_pkg_1", "author": "test_user", "type": "showcase"}
        ]

    metastore_client = metastore.create_metastore("filesystem", dict(uri="mem://"))
    number_of_datasets = migrator.migrate_datasets((datasets), metastore_client)

    assert number_of_datasets == 1
