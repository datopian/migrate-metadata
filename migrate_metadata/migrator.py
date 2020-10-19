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

LOG_FORMAT = '%(asctime)-15s %(name)-15s %(levelname)s %(message)s'


def migrate_datasets(datasets, metastore_client):
    """Migrate all datasets in an iterable to metastore
    """
    datapackages = (
        ckan_to_frictionless.dataset(ds) for ds in datasets if ds['type'] == 'dataset'
        )
    stored = 0
    for package in datapackages:
        log.debug("Converted dataset to datapacakge: %s", package)
        try:
            author = _get_author(package)
            metastore_client.create(package['name'], package, author=author)
            stored += 1
            log.debug("Successfully stored package: %s", package['name'])
        except Conflict:
            log.info("Package already exists in metastore backend: %s", package['name'])
        except Exception:
            log.exception("Failed storing package: %s", package['name'])
    return stored


def _get_author(package):
    """Extract author object from datapackage
    """
    try:
        package_author = filter(lambda c: c['role'] == 'author', package['contributors'])[0]
        return Author(package_author['name'], package_author['email'])
    except (KeyError, IndexError):
        return None


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
@click.option('--include-private', is_flag=True, help='Include private datasets in the migration')
@click.option('--include-drafts', is_flag=True, help='Include drafts datasets in the migration')
@click.option('--rows', type=int, default=100, help='Number of rows to fetch per API call to package_search. Default: 100.')
@click.option('--verbose', '-v', count=True, help='control output verbosity')
def main(ckan_api_url, ckan_api_key, metastore_type, metastore_options, include_private, include_drafts, rows, verbose):
    """Import all CKAN datasets into a metastore-lib backend
    """
    if verbose > 1:
        level = logging.DEBUG
    elif verbose > 0:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(level=level, format=LOG_FORMAT)

    ckan_client = CkanAPIClient(ckan_api_url, ckan_api_key)
    metastore_client = create_metastore(metastore_type, metastore_options)

    params = {
            'include_private': include_private,
            'include_drafts': include_drafts,
            'rows': rows,
        }
    click.echo("Starting the migration from: {}".format(ckan_api_url))
    datasets = ckan_client.get_datasets_list_from_search(params)
    result = migrate_datasets(datasets, metastore_client)
    click.echo("Successfully migrated {} datasets".format(result))


if __name__ == '__main__':
    main()
