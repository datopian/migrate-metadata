"""Main migrator script module

This can be used as a CLI command, run wit `--help` for more information
"""
import json
import logging

import click
from frictionless_ckan_mapper import ckan_to_frictionless
from metastore import create_metastore
from metastore.backend.exc import Conflict
from metastore.types import Author

from .ckan_api import CkanAPIClient

log = logging.getLogger(__name__)


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


class JsonParamType(click.ParamType):
    """JSON serialized object as a click parameter
    """
    name = "json"
    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except TypeError:
            self.fail(
                "expected string for json conversion, got {!r} of type {}".format(value, type(value).__name__),
                param,
                ctx,
            )
        except ValueError:
            self.fail("{value!r} is not valid JSON".format(value=value), param, ctx)


@click.command()
@click.option('--ckan-api-url', '-c', type=str, required=True, help='URL of the CKAN instance API')
@click.option('--ckan-api-key', '-k', type=str, required=True, help='CKAN API key')
@click.option('--metastore-type', '-m', type=str, required=True, help='metastore-lib backend type')
@click.option('--metastore-options', '-o', type=JsonParamType(), default={}, help='metastore-lib options')
def main(ckan_api_url, ckan_api_key, metastore_type, metastore_options):
    """Import all CKAN datasets into a metastore-lib backend
    """
    ckan_client = CkanAPIClient(ckan_api_url, ckan_api_key)
    metastore_client = create_metastore(metastore_type, metastore_options)
    result = migrate_all_datasets(ckan_client, metastore_client)
    click.echo("Successfully migrated {} datasets".format(result))


if __name__ == '__main__':
    main()
