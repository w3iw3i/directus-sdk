import argparse, os, sys, json
from directus.clients import DirectusClient_V9
'''
usage:
python directus_v9_migration.py -c collection_a collection_b 
'''


def parse_arguments():
    parser = argparse.ArgumentParser()
    # nargs = '+' takes 1 or more arguments, '*' takes 0 or more
    parser.add_argument(
        '-c',
        '--collections',
        nargs='+',
        type=str,
        required=False,
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

    DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD')

    api_1 = DirectusClient_V9(DIRECTUS_FROM_URL, DIRECTUS_FROM_TOKEN)
    api_2 = DirectusClient_V9(DIRECTUS_TO_URL, DIRECTUS_TO_TOKEN)

    print('migrating collection schemas...')
    # get collections for api_1
    user_collection_names = api_1.get_all_user_created_collection_names()

    # post collections for api_2
    for collection in user_collection_names:
        collection_schema = api_1.get(f"/collections/{collection}")
        if api_1.get_pk_field(collection)[
            'field'
        ] != 'id' or api_1.get_pk_field(collection)['type'] != 'integer':
            collection_schema['fields'] = [{
                'field':
                api_1.get_pk_field(collection)['field'],
                'type':
                api_1.get_pk_field(collection)['type'],
                'meta': {
                    "interface": "input",
                    "readonly": False,
                    "hidden": False
                },
                "schema": {
                    "has_auto_increment": False,
                    "is_primary_key": True,
                    "length": 255
                }
            }]
            field_data = [
                field for field in api_1.get_all_fields(collection)
                if not field['schema']['is_primary_key']
            ]
            api_2.post(f"/collections", json=collection_schema)
            for field in field_data:
                api_2.post(f'/fields/{collection}', json=field)

        print('migrating relations...')
        relations = [
            col for col in api_1.get('/relations')
            if not col['collection'].startswith('directus')
        ]
        for relation in relations:
            api_2.post(f'/relations', json=relation)

        # get roles for api_1
        print('migrating roles...')
        roles = api_1.get('/roles', params={"limit": -1})
        for role in roles:
            if 'users' in role.keys():
                role.pop('users')
            role_id = api_2.post('/roles', json=role)['data']['id']
            permissions = api_1.get(
                f'/permissions?filter[role][_eq]={role_id}'
            )
            for permission in permissions:
                if 'id' in permission.keys():
                    permission.pop('id')
                api_2.post('/permissions', json=permission)

        print('migrating users...')
        users = api_1.get('/users', params={"limit": -1})
        for user in users:
            user['password'] = DEFAULT_PASSWORD
            api_2.post('/users', json=user)

        print('migrating data...')
        for collection in args.collections:
            data = api_1.get(f'/items/{collection}', params={"limit": -1})
            for i in range(0, len(data), 100):
                api_2.post(f'/items/{collection}', json=data[i:i + 100])

        print('migrating webhooks...')
        webhooks = api_1.get(f'/webhooks?fields=name,actions,collections,url')
        for webhook in webhooks:
            api_2.post(f'/webhooks', json=webhook)

        print('migrating files...')
        files = api_1.get('/files')
        if len(files) > 0:
            for file in files:
                id = file['id']
                file.pop('id')
                postData = {}
                postData['data'] = file
                postData[
                    'url'
                ] = f'http://{DIRECTUS_FROM_TOKEN}/assets/{id}?download&access_token={DIRECTUS_FROM_TOKEN}'
                api_2.post('/files/import', json=postData)
        print('finished migration!')


if __name__ == '__main__':
    main()
