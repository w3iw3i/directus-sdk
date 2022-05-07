# This is a temporary script run to transfer only the items in each collection. Used to migrate dat from v8 to an already running v9 instance.
# v8-v9 migration is run once to an intermediary (temp) v9 instance, and this script is run to migrate the items from the intermediary to the v9 prod.
# This involves removing all items in the v9 production instance, and transferring the items from v8 instead.
# Remember to remove all webhooks set to the collections before running the code.
import argparse, os, sys
from directus.clients import DirectusClient_V9


def parse_arguments():
    parser = argparse.ArgumentParser()
    # nargs = '+' takes 1 or more arguments, '*' takes 0 or more
    parser.add_argument(
        '-c',
        '--collections',
        nargs='+',
        type=str,
        required=True,
        default="test",
        help='<Required> Names of directus collections to create staging tables'
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    DIRECTUS_FROM_URL = os.environ.get('DIRECTUS_FROM_URL')
    DIRECTUS_FROM_TOKEN = os.environ.get('DIRECTUS_FROM_TOKEN')

    DIRECTUS_TO_URL = os.environ.get('DIRECTUS_TO_URL')
    DIRECTUS_TO_TOKEN = os.environ.get('DIRECTUS_TO_TOKEN')

    api_1 = DirectusClient_V9(DIRECTUS_FROM_URL, DIRECTUS_FROM_TOKEN)
    api_2 = DirectusClient_V9(DIRECTUS_TO_URL, DIRECTUS_TO_TOKEN)

    print('migrating data...')
    for collection in reversed(list(args.collections)):
        print(f"deleting records from {collection}")
        # delete data from api_2
        try:
            api_2.delete_all_items(collection)
        except AssertionError as e:
            if str(e) == 'No items to delete!':
                print(str(e))
                pass
            else:
                raise

    for collection in args.collections:
        print(f"migrating records into {collection}")
        data = api_1.get(f'/items/{collection}', params={"limit": -1})
        tempData = data.copy()
        for i in range(len(tempData)):
            if "modified_by" in tempData[i].keys():
                del tempData[i]["modified_by"]

        api_2.bulk_insert(collection, tempData)

    print('Finished migration!')


if __name__ == '__main__':
    main()
