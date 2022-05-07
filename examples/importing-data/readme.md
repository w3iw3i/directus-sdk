# Importing data into directus

`import_single.py` is a script to import csv file data into an existing collection in directus. In general, the workflow to import data into directus is to get the requirements for the database tables from the users, and manually create the collection on directus using the GUI, then use API access to import data into that collection.

## Usage
```
usage: import_single.py [-h] [--fpath FPATH] [--collection COLLECTIONS] [--url URL] [--token TOKEN] [--delete_existing]

Script to import .csv data into existing collection

optional arguments:
    -h, --help              show this help message and exit
    --fpath FPATH           Path to .csv file, collection name will be the name of the file
    --collection COLLECTIONS
                            <Required> Names of directus collections to migrate
    --url URL               <Required> URL to directus
    --token TOKEN           Admin user access token
    --delete_existing       Set true to delete existing data from directure before importing
```