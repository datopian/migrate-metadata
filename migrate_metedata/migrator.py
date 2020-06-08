import logging

from Ckan_API.Ckan_API import CkanAPICall
import ckan_datapackage_tools.converter as converter
import metastore.backend as metastore

log = logging.getLogger(__name__)


def wrapper(ckan_api_url, ckan_api_key, metastore_type, metastore_options):
    ckan_client = CkanAPICall(ckan_api_url, ckan_api_key)
    metastore_client = metastore.create_metastore(metastore_type, **metastore_options)
    return migrate_all_datasets(ckan_client, metastore_client)

def migrate_all_datasets(ckan_client, metastore_client):
    datapackages = (converter.dataset_to_datapackage(ds) for ds in ckan_client.get_all_datasets())
    stored = 0
    for package in datapackages:
        try:
            metastore_client.create(package['name'], package)
            stored += 1
        except metastore.exc.Conflict:
            log.info("package already exists")
        except Exception:
            log.error("failed storing package: %s", package['name'])
    return stored
