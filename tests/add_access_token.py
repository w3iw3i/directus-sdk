import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from directus.clients import DirectusClient_V9
import os

url = os.environ.get("BASE_URL", "http://localhost:8055")
email = os.environ.get("ADMIN_EMAIL", "admin@example.com"),
password = os.environ.get("ADMIN_PASSWORD", "password")

client = DirectusClient_V9(url=url, email=email, password=password)

id = client.get("/users/me")['id']

client.patch(f'/users/{id}', json={"token": "admin"})

