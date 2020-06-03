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
        self.new_metastore = new_metastore
        self.config = options

    def migrate_dataset(self, pkg_name):
        urlpath = self.ckan_classic_api + '/package_show?id=' + pkg_name

        response = json.loads(urllib.urlopen(urlpath).read())
        pkg_dict = response['result']

        package_id = pkg_dict["id"]
        data_package_json = converter.dataset_to_datapackage(pkg_dict)

        try:
            metastore_client = store.create_metastore(self.new_metastore, **self.config)
            package_info = metastore_client.create(package_id, data_package_json)
        except Exception as e:
            log.info("{} dataset is already exists".format(pkg_name))

    def migrate_all_datasets(self):
        urlpath = self.ckan_classic_api + '/package_list'

        try:
            response = json.loads(urllib.urlopen(urlpath).read())
            pkgs_list = response['result']
        except ValueError as e:
            log.info("There is no dataset available in your CKAN")

        for pkg_name in pkgs_list:
            self.migrate_dataset(pkg_name)