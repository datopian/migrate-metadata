import urllib
import json
import logging

import ckan_datapackage_tools.converter as converter
import metastore.backend as store

log = logging.getLogger(__name__)


class Migrator:
    """Migrator of metadata from one store to another
    """

    def __init__(self, ckan_classic_api, new_metastore, options):
        self.ckan_classic_api = ckan_classic_api
        self.metastore_client = store.create_metastore(new_metastore, **options)

    def migrate_dataset(self, pkg_name):
        urlpath = self.create_url('/package_show?id=', pkg_name)
        response = json.loads(urllib.urlopen(urlpath).read())
        self.create_pkg(response, pkg_name)

    def migrate_all_datasets(self):
        urlpath = self.create_url('/package_list')
        response = json.loads(urllib.urlopen(urlpath).read())
        self.iterate_pkgs(response)

    def create_url(self, suffix, pkg_name=''):
        url = self.ckan_classic_api + suffix
        url += pkg_name
        return url

    def create_pkg(self, data, pkg_name):
        pkg_dict = data.get('result')

        if pkg_dict:
            data_package_json = converter.dataset_to_datapackage(pkg_dict)

            try:
                package_info = self.metastore_client.create(pkg_name, data_package_json)
                return True
            except store.exc.Conflict as e:
                log.info("{} dataset already exists".format(pkg_name))
                return False

        return False

    def iterate_pkgs(self, data):
        pkgs_list = data.get('result')
        if not pkgs_list:
            raise ValueError("There is no dataset available in your CKAN")

        for pkg_name in pkgs_list:
            self.migrate_dataset(pkg_name)
