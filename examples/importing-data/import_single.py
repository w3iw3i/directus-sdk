import argparse, os
import requests, json
import pandas as pd
import copy, sys
import csv
from directus.clients import DirectusClient_V9
from getpass import getpass, getuser
import warnings


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Script to import .csv data into existing collection"
    )

    parser.add_argument(
        '--fpath',
        type=str,
        required=True,
        help=
        '<Required> Path to .csv file. Collection name will be the name of the file'
    )
    parser.add_argument(
        '--collection',
        type=str,
        required=True,
        help='<Required> Names of directus collection to import'
    )
    parser.add_argument(
        '--url',
        type=str,
        required=False,
        default="http://localhost:8055",
        help='<Required> URL to directus'
    )
    parser.add_argument(
        '--token', default='admin', type=str, help="Admin user access token"
    )
    # parser.add_argument(
    #     '--username', type=str, required=False, help='username prompt'
    # )
    # parser.add_argument(
    #     '--password',
    #     type=str,
    #     required=False,
    #     default='',
    #     help=argparse.SUPPRESS
    # )
    parser.add_argument(
        '--delete_existing',
        action="store_true",
        default=False,
        help="Set true to delete existing data from directus before importing"
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    # if not args.username:
    #     args.username = getuser()
    # if args.password:
    #     warnings.warn(
    #         'User set the password in plain text and instead should just omit --password'
    #     )
    # else:
    #     args.password = getpass(prompt="Enter Password:")
    api = DirectusClient_V9(args.url, args.token)
    field_names = [
        col['field'] for col in api.get(f'/fields/{args.collection}')
        if col['field'] != 'id'
    ]

    if os.path.isfile(args.fpath):
        df = pd.read_csv(
            args.fpath, dtype=object, parse_dates=field_names
        )  # dtype=object so that it will use python default data types to make sure its all json-serializable
        # CSV could have been saved along with an (unnamed) index (RangeIndex). Could be due to running pd.to_csv(fname) without index=False
        # stackoverflow.com/questions/36519086
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        # df = df.fillna(
        #     ''
        # )   # empty values will be stored as np.nan. We want to convert it to empty string for directus
        print(f"reading {args.fpath}")
    else:
        print(f"{args.fpath} is not a valid file!")
        return

    df.columns = [
        col.lower().strip().replace(" ", "_") for col in list(df.columns)
    ]
    directus_collection_colnames = [
        col['field'] for col in api.get(f'/fields/{args.collection}')
        if col['field'] != "id"
    ]

    # Checking for system default fields in the directus collections that are not in the csv files, and remove them from the matching condition
    directus_system_fields = [
        'status', 'sort', 'date_created', 'user_created', 'date_updated',
        'user_updated'
    ]
    system_fields_to_remove = [
        field for field in directus_collection_colnames
        if field in directus_system_fields if field not in df.columns
    ]
    directus_collection_colnames = [
        col for col in directus_collection_colnames
        if col not in system_fields_to_remove
    ]

    print(f"Cleaned file column names: \t{sorted(list(df.columns))}")
    print(
        f"directus file column names: \t{sorted(directus_collection_colnames)}"
    )

    match = True

    for colname in directus_collection_colnames:
        if colname not in list(
            df.columns
        ) and not api.get(f'/fields/{args.collection}/{colname}')['schema'][
            'is_nullable'
        ] and api.get(f'/fields/{args.collection}/{colname}'
                      )['schema']['default_value'] is None:
            print(colname)
            match = False

    if match:
        print("Column names match between file and directus collection")
    else:
        print("Column names does not match!")
        return

    # data = []
    # for i in range(len(df)):
    #     data.append(df.iloc[i].to_dict())

    data = json.loads(df.to_json(orient='records', date_format="iso"))

    print(f"Number of entries: {len(df)}")
    print(df.describe())

    if args.delete_existing:
        print("Deleting existing data...")
        api.delete_all_items(args.collection)

    print("Uploading items...")
    api.bulk_insert(args.collection, data)

    print("Upload successful!")


if __name__ == '__main__':
    main()
