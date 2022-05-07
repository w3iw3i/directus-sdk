# v9 to v9 migration tool
This script migrates all users and data from one v9 instance to another v9 instance. Passwords are reset as directus does not allow retrieval of user passwords.

## .env
Fill in all values in the `example.env` file and rename it to `.env` before running the script.

## How to run:
```
usage: directus_v9_migration.py [-h] [-c COLLECTIONS [COLLECTIONS ...]]

optional arguments:
    -h, --help              show this help message and exit
    -c COLLECTIONS [COLLECTIONS ...], --collections COLLECTIONS [COLLECTIONS ...]
                            <Required> Names of directus collections to migrate
```

```
python directus_v9_migration.py -c collection_a collection_b collection_c
```

## Updating existing v9 collections from existing v9
For the use case of updating items in v9 from another existing v9, run `update_v9.py`. Configure the `.env` file with the v9 access token before running the script.

```
usage: update_v9.py [-h] [-c COLLECTIONS [COLLECTIONS ...]]

optional arguments:
    -h, --help              show this help message and exit
    -c COLLECTIONS [COLLECTIONS ...], --collections COLLECTIONS [COLLECTIONS ...]
                            <Required> Names of directus collections to update
```

```
python update_v9.py -c collection_a collection_b collection_c
```
