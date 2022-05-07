import argparse, os
import requests, json
import pandas as pd
import copy, sys
from directus.clients import DirectusClient_V9


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Script to remove duplicate records in existing collection"
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
        help=
        '<Required> Names of directus collections to remove duplicate records'
    )
    parser.add_argument(
        '--token', default='admin', type=str, help="Admin user access token"
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    api = DirectusClient_V9(args.url, args.token)
    for collection in args.collections:
        print(f"{'='*50} {collection} {'='*50}")
        field_names = [
            col['field'] for col in api.get(f'/fields/{collection}')
            if col['field'] != 'id'
        ]
        data = pd.DataFrame(
            api.get(f'/items/{collection}', params={"limit": -1})
        )
        duplicate_ids = data[data.duplicated(subset=field_names
                                             )]['id'].tolist()
        if len(duplicate_ids) == 0:
            print("No duplicate record found!")
            continue
        else:
            print(f"{len(duplicate_ids)} duplicate records found")
        print("Deleting duplicate records...")
        for i in range(0, len(duplicate_ids), 100):
            api.delete(f'/items/{collection}', json=duplicate_ids[i:i + 100])
        print("All duplicate records have been deleted!")


if __name__ == '__main__':
    main()
