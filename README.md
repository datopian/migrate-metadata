# Migrate Metadata
Migrate Metadata is a tool to migrate all datasets from a CKAN instance to a
[metastore-lib](https://github.com/datopian/metastore-lib) backend such as GitHub or
a local filesystem.

## Installation

Currently `migrate-metadata` has support for Python 2.7 only.

First, clone the repo via git:

```bash
$ git clone https://github.com/datopian/migrate-metadata.git
```

Move to directory:

```bash
$ cd migrate-metadata
```
Install all requirements and the package (it is recommended that this is done in a virtual environment):

```bash
$ pip install -r requirements.txt .
$ python setup.py develop
```

## Usage

To import all CKAN datasets into a metastore backend, run:

```bash
$ metastore-import-ckan -c $CKAN_API_URL -k $CKAN_API_KEY \
                        -m $METASTORE_TYPE -o $METASTORE_OPTIONS
```

Replace all environment variables above with relevant values.

* `$METASTORE_TYPE` should be a metastore-lib backend type
* `$METASTORE_OPTIONS` should be a JSON-serialized object with the configucation options expected by the
specific metastore-lib backend you are using.

See [the metastore-lib documentation](https://metastore-lib.readthedocs.io/en/latest/backends/index.html)
for a list of supported backends and their respective configuration options.

Run `metastore-import-ckan --help` to get the full list of
command line options.

## Examples

Import all CKAN datasets from http://ckan:500 to a local filesystem metastore in ./metastore:
```bash
$ metastore-import-ckan -c http://ckan:5000 -k 123-abc-321-xyz \
                        -m filesystem -o '{"uri":"./metastore"}'
```

Import all CKAN datasets from http://ckan:500 to a private GitHub repository:
```bash
$ GITHUB_OPTS='{
    "github_options": {"login_or_token": "averylongtokenthatwasgeneratedespeciallyforthis"},
    "private":true,
    "default_owner":"myorganization"}'
$ metastore-import-ckan -c http://ckan:5000 -k 123-abc-321-xyz \
                        -m github -o "$GITHUB_OPTS"
```

The `jq` command line tool can be useful to debug the output of the migration process
while working locally. For example, to list all datasets migrated you can execute:
```bash
$ cat $(ls  metastore/p/*/* | grep -v '\.') | jq '.title'
```

## Tests

To run tests:

```bash
make test
```

## License

This project is licensed under the MIT License - see the [LICENSE](License) file for details
