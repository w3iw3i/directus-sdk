import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from directus.clients import DirectusClient_V9
import os

url = os.environ.get("BASE_URL", "http://localhost:8055")

client = DirectusClient_V9(url=url, email="admin@example.com", password="password")

id = client.get("/users/me")['id']

client.patch(f'/users/{id}', json={"token": "admin"})

