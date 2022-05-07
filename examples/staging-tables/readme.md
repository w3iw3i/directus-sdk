# Utility to generate staging tables

status-config.json contains the configuration for the colored button for status in the directus field.

## config.json

The script takes in an optional .json file which has the configuration of any status buttons you want to add in as well. This repo has a few examples of status
configuration for reference.

## Usage
```
usage: generate_staging_tables.py [-h] [--url URL] [-c COLLECTIONS [COLLECTIONS ...]] [--token TOKEN] [--status STATUS]

optional arguments:
    -h, --help              show this help message and exit
    --url URL               <Required> URL to directus
    -c COLLECTIONS [COLLECTIONS ...], --collections COLLECTIONS [COLLECTIONS ...]
                            <Required> Names of directus collections to migrate
    --token TOKEN           Admin user access token
    --status STATUS         File path to the status-config.json configuration file for how the status column should be added. No status column will be generated if it is not specified.
```