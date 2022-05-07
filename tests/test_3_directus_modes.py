import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from directus.clients import DirectusClient_V9
import pytest
'''
This script tests the functionality of login, logout, and refresh
'''
client = DirectusClient_V9(url=os.environ.get("BASE_URL", "http://localhost:8055"), token="admin")


@pytest.mark.parametrize(
    "collection_name, pk_type", [("test_collection", "int")]
)
def test_create_collection(collection_name: str, pk_type: str):
    collection_data = {"collection": collection_name, "schema": {}, "meta": {}}
    if pk_type == "uuid":
        collection_data['fields'] = [{
            "field": "id",
            "type": "uuid",
            "meta": {
                "hidden": True,
                "readonly": True,
                "interface": "text-input",
                "special": ["uuid"]
            },
            "schema": {
                "is_primary_key": True
            }
        }]
    assert client.post(
        f"/collections", json=collection_data
    )['data']['collection'] == collection_name


@pytest.mark.parametrize(
    "collection_name, field_name, field_type",
    [("test_collection", "name", "string")]
)
def test_login_modes(collection_name: str, field_name: str, field_type: str):
    try:
        client.post(
            f"/fields/{collection_name}",
            json={
                "field": field_name,
                "type": field_type
            }
        )
        client.logout()
        client.static_token = "admin"
        client.delete(f"/fields/{collection_name}/{field_name}")
        client.static_token = None
        client.login(email="admin@example.com", password="password")
        client.post(
            f"/fields/{collection_name}",
            json={
                "field": field_name,
                "type": field_type
            }
        )
    except Exception as e:
        print(e)
        
        
@pytest.mark.parametrize(
    "collection_name", 
    [
        ("test_collection")
    ]
)
def test_delete_collection(collection_name: str):
    client.delete(f"/collections/{collection_name}")
    assert client.get(f"/collections/{collection_name}") == None