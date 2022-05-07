import argparse, os
import requests, json
import copy, sys
from directus.clients import DirectusClient_V9


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Script to generate staging tables using existing collection"
    )

    parser.add_argument(
        '--url',
        type=str,
        required=False,
        default="http://localhost:8055",
        help='<Required> URL to directus'
    )
    # nargs = '+' takes 1 or more arguments, '*' takes 0 or more
    parser.add_argument(
        '-c',
        '--collections',
        nargs='+',
        type=str,
        required=True,
        help='<Required> Names of directus collections to create staging tables'
    )
    parser.add_argument(
        '--token', default='admin', type=str, help="Admin user access token"
    )
    parser.add_argument(
        '--status',
        type=str,
        default=None,
        required=False,
        help=
        "File path to the status.json configuration for how the status column should be added. No status column will be generated if it is not specified."
    )
    return parser.parse_args()


def create_staging_collection(api: DirectusClient_V9, collection_name: str):
    # get request to get collections
    # get request to get fields from the collection, and remove all 'id' keys from the json
    # add 'fields' key to collection data
    # replace all base_collection to staging_collection
    # post it
    collection_data = api.get(f'/collections/{collection_name}')
    postData = copy.deepcopy(collection_data)
    for k, v in collection_data.items():
        if v == collection_name:
            postData[k] = v + '_staging'
        elif isinstance(v, dict):
            for k2, v2 in v.items():
                if v2 == collection_name:
                    postData[k][k2] = v2 + '_staging'

    api.post(f'/collections', json=postData)


def migrate_fields(api: DirectusClient_V9, collection_name: str):
    field_data = api.get(f'/fields/{collection_name}')
    if field_data[0]['field'] == 'id':
        field_data = field_data[1:]
    for field in field_data:
        if field['schema'] is not None:
            field['schema'].pop('table')
            if field['schema']['foreign_key_table'] is not None:
                field['schema']['foreign_key_table'] += '_staging'

        field.pop('collection')
        field['meta'].pop('id')
        field['meta'].pop('collection')
        api.post(f'/fields/{collection_name + "_staging"}', json=field)


def migrate_relations(api: DirectusClient_V9, collection_name: str):
    # get relations
    relations = api.get(f'/relations/{collection_name}')
    postData = [{
        "collection":
        relation["collection"] + "_staging",
        "field":
        relation["field"],
        "related_collection":
        relation["related_collection"] + "_staging"
        if not relation["related_collection"].startswith('directus') else
        relation["related_collection"]
    } for relation in relations]

    for relation in postData:
        api.post_relation(relation)


def duplicate_data(api: DirectusClient_V9, collection_name: str):
    data = api.get(f'/items/{collection_name}', params={"limit": -1})
    if len(data) == 0:
        print(f'No data found on {collection_name}, skipping this step...')
        return
    for i in range(0, len(data), 100):
        api.post(
            f'/items/{collection_name + "_staging"}', json=data[i:i + 100]
        )


def create_status_field(api, status_fpath, collection_name):
    # read status-config.json file
    if not os.path.isfile(status_fpath):
        raise AssertionError(f"{status_fpath} is not a file, exiting...")
    with open(status_fpath, "r") as f:
        status_fields = json.load(f)

    for field in status_fields:
        api.post(f'/fields/{collection_name}', json=field)
        field['schema']['default_value'] = 'draft'
        api.patch(f'/fields/{collection_name}/{field}', json=field)


def main():
    args = parse_arguments()
    api = DirectusClient_V9(args.url, args.token)
    directus_collections = api.get('/collections')
    collection_names = [
        col for col in directus_collections
        if not col['collection'].startswith('directus')
    ]
    collection_names = [
        collection["collection"] for collection in collection_names
    ]
    for collection in args.collections:
        print(f"{'='*50} {collection} {'='*50}")
        if collection + "_staging" in collection_names:
            print(
                f"Staging collection for {collection} already exists, skipping..."
            )
            continue
        elif collection in collection_names:
            if args.status is not None:
                print(f"creating status field...")
                create_status_field(api, args.status, collection)
            print(f"Creating staging collection for {collection}")
            create_staging_collection(api, collection)
            print(f"Migrating fields (columns) to staging collection")
            migrate_fields(api, collection)
            print(
                f"Migrating relations from {collection} to {collection}_staging"
            )
            migrate_relations(api, collection)
            print(
                f"Duplicating data from {collection} to {collection}_staging"
            )
            duplicate_data(api, collection)


if __name__ == '__main__':
    main()
