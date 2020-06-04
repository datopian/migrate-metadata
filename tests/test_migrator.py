# from mock import patch

from migrate_metedata.migrator import Migrator
import metastore.backend as store

migrator_obj = Migrator('https://demo.ckan.org/api/3/action', 'filesystem', dict(uri='mem://'))


class TestMigrator:

    def test_create_url_with_pkg(self):
        suffix = '/package_show?id='
        pkg_name = 'world-population'
        url = 'https://demo.ckan.org/api/3/action' + suffix + pkg_name

        assert migrator_obj.create_url(suffix, pkg_name) == url

    def test_create_url_without_pkg(self):
        suffix = '/package_list'
        url = 'https://demo.ckan.org/api/3/action' + suffix

        assert migrator_obj.create_url(suffix) == url

    def test_create_pkg(self):
        data = {"result": {"name": "test_pkg",
               "resources": [
                   {"path": "data/myresource.csv"}
               ]}}
        pkg_name = "test_pkg"

        assert migrator_obj.create_pkg(data, pkg_name) == True

    # @patch('Migrator.urllib.urlopen')
    # def test_getting_todos(self, mock_urlopen):
    #     pass
