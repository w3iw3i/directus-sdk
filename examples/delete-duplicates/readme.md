# Delete duplicate data in Directus

`delete_duplicates.py` is a script to remove duplicate data in directus collections. It utilises pandas dataframe to 

## Usage
```
usage: delete_duplicates.py [-h] [-c COLLECTIONS [COLLECTIONS ...]] [--url URL] [--token TOKEN]

Script to remove duplicate records in directus collections

optional arguments:
    -h, --help              show this help message and exit
    -c COLLECTIONS [COLLECTIONS ...], --collections COLLECTIONS [COLLECTIONS ...]
                            <Required> Names of directus collections to remove duplicates
    --url URL               <Required> URL to directus
    --token TOKEN           Admin user access token
```