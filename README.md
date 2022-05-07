# Directus Python SDK

> This software development kit is meant to be used with Directus[https://directus.io/]. Anu updates to the SDK would require reinstalling the package via pip.

## Requirements

- Python 3.6+

## Installation

Simply install the pip module by running:

```bash
pip install -e .
```

## Setup environment variables

Add a .env file in the project folder with the following environment variables:

POSTGRES_HOST=xxxx
POSTGRES_DB=xxxx
POSTGRES_USER=xxxx
POSTGRES_PASSWORD=xxxx
ADMIN_EMAIL=xxxx
ADMIN_PASSWORD=xxxx

## Examples

Examples of using the directus clients are provided in the `examples/` folder. These scripts are used to automate the execution of the common tasks required in maintaining local deployment of Directus.

Run pip install command below to install the dependencies to run the examples scripts
```bash
pip install -r examples/requirements.txt
```

## Usage

### Intialize directus client

```python
from directus.clients import DirectusClient_V9

# Create a directus client connection with user static token
client = DirectusClient_V9(url="http://localhost:8055", token="admin")


# Create a directus client connection with user email and password
client = DirectusClient_V9(url="http://localhost:8055", email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
```

### Logging in and out of the client

```python
client = DirectusClient_V9(url="http://localhost:8055", email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
# Log out and use static token instead
client.logout()
client.static_token = "admin"
# make sure to set static token to None before using a temporary token with the login command
client.static_token = None
client.login(email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
```

### Generic API requests

The directus client automatically handles the injection of static access token so any [directus API requests](http://localhost:8055) can be simplified like so:

```python
# GET request
collection  = client.get(f"/collections/{collection_name}")
item        = client.get(f"/items/{collection_name}/1")

# POST request
items = [
    {
        "name": "item1"
    },
    {
        "name": "item2"
    }
]

client.post(f"/items/{collection_name}", json=items)

# PATCH request
client.patch(f"/items/{collection_name}/1", json={
    "name": "updated item1"
})

# DELETE request
client.delete(f"/items/{collection_name}/1")
```

#### Bulk Insert

> **Params:** collection_name: str, items: list

```python
client.bulk_insert(collection_name="test-collection",
            items=[{"Title": "test"}, {"Title": "test2"}])
```

#### Duplicate Collection

> **Params:** collection_name: str, duplicate_collection_name: str

```python
client.duplicate_collection(collection_name="test_collection", duplicate_collection_name="test_duplicate_collection")
```

#### Checks if collection exists

> **Params:** collection_name: str, items: list

```python
if client.collection_exists("brands"):
    print("brands collection exists!")
```

#### Delete all items from a collection

> **Params:** collection_name: str

```python
client.delete_all_items("brands")
```

#### Get collection primary key

> **Params:** collection_name: str

```python
pk_field = client.get_pk_field("brands")
```

#### Get all user-created collection names

> **Params:**

```python
print("Listing all user-created collections on directus...")
for name in client.get_all_user_created_collection_names():
    print(f"{name})
```

#### Get all field names of a given collection

> **Params:** collection_name: str

```python
print("Listing all fields in collection...")
for field in client.get_all_fields("collection"):
    print(json.dumps(field, indent=4))
```

#### Get all foreign key fields in directus collection

> **Params:** collection_name: str

```python
print("Listing all foreign key fields in collection...")
for field in client.get_all_fk_fields("collection"):
    print(json.dumps(field, indent=4))
```

#### Get all relations in directus collection

> **Params:** collection_name: str

```python
import json
print("Listing all relations in collection...")
for field in client.get_relations("collection"):
    print(json.dumps(field, indent=4))
```

#### Create relations

> **Params:** relation: dict

```python
client.post_relation({
    "collection": "books",
    "field": "name",
    "related_collection": "authors"
})
```