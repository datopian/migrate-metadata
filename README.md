# Migrate Metadata

Migrate Metadata is a lib to store datasets from ckan to some other store (like github, filesystem)

## Install

First, clone the repo via git:

```bash
$ git clone git@github.com:datopian/ckan3-py-sdk.git
```

Move to directory:

```bash
$ cd
```
Install the package:

```bash
$ python setup.py install
```

## Developers
```bash
from migrate_metedata import migrator

datasets_stored = migrator.wrapper(ckan_api_url, ckan_auth_token, store, configs)

# e.g. if store is filesystem
datasets_stored = migrator.wrapper("http://ckan:5000", "123-abc-321-xyz", "filesystem", {"uri": "mem://"})
```

## Tests

To run tests:

```bash
 pytest tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](License) file for details
