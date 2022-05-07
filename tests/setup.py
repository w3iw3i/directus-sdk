import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from directus.clients import DirectusClient_V9
import uuid


def main():
    client = DirectusClient_V9(
        url=os.environ.get("BASE_URL", "http://localhost:8055"),
        email="admin@example.com",
        password="password"
    )
    collection_data = {
        "collection": "test_collection",
        "schema": {},
        "meta": {}
    }
    client.post("/collections", json=collection_data)
    field_data = [{
        "field": "name",
        "type": "string",
        "schema": {},
        "meta": {}
    }, {
        "field": "comments",
        "type": "text",
        "schema": {},
        "meta": {}
    }]
    for field in field_data:
        client.post("/fields/test_collection", json=field)
    items = [{
        "name": str(i) + str(uuid.uuid4()),
        "comments": str(uuid.uuid4())
    } for i in range(10)]
    client.bulk_insert("test_collection", items)


if __name__ == '__main__':
    main()
