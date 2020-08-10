import logging

from frictionless_ckan_mapper import ckan_to_frictionless
from metastore import create_metastore
from metastore.backend.exc import Conflict
from metastore.types import Author

from .ckan_api import CkanAPIClient

log = logging.getLogger(__name__)


def wrapper(ckan_api_url, ckan_api_key, metastore_type, metastore_options):
    ckan_client = CkanAPIClient(ckan_api_url, ckan_api_key)
    metastore_client = create_metastore(metastore_type, metastore_options)
    return migrate_all_datasets(ckan_client, metastore_client)


def migrate_all_datasets(ckan_client, metastore_client):
    """Migrate all datasets in the CKAN database to metastore
    """
    return migrate_datasets(ckan_client.get_all_datasets(), metastore_client)


def migrate_datasets(datasets, metastore_client):
    """Migrate all datasets in an iterable to metastore
    """
    datapackages = (ckan_to_frictionless.dataset(ds) for ds in datasets)
    stored = 0
    for package in datapackages:
        try:
            package_author = package['author']
            author = Author(package_author['name'], package_author['email'])
            metastore_client.create(package['name'], package, author=author)
            stored += 1
        except Conflict:
            log.info("package already exists")
        except Exception:
            log.exception("failed storing package: %s", package['name'])
    return stored
