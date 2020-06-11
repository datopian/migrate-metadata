import logging

from ckan_api.ckan_api import CkanAPIClient
import ckan_datapackage_tools.converter as converter
import metastore.backend as metastore
from metastore.types import Author

log = logging.getLogger(__name__)


def wrapper(ckan_api_url, ckan_api_key, metastore_type, metastore_options):
    ckan_client = CkanAPIClient(ckan_api_url, ckan_api_key)
    metastore_client = metastore.create_metastore(metastore_type, metastore_options)
    return migrate_all_datasets(ckan_client, metastore_client)

def migrate_all_datasets(ckan_client, metastore_client):
    datapackages = (converter.dataset_to_datapackage(ds) for ds in ckan_client.get_all_datasets())
    stored = 0
    for package in datapackages:
        try:
            package_author = package['author']
            author = Author(package_author['name'], package_author['email'])

            metastore_client.create(package['name'], package, author=author)
            stored += 1
        except metastore.exc.Conflict:
            log.info("package already exists")
        except Exception:
            log.exception("failed storing package: %s", package['name'])
    return stored
