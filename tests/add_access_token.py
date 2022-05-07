from directus.clients import DirectusClient_V9
import os

client = DirectusClient_V9(
    url=os.environ.get("BASE_URL", "http://localhost:8055"),
    email=os.environ.get("ADMIN_EMAIL", "admin@example.com"),
    password=os.environ.get("ADMIN_PASSWORD", "password")
)

id = client.get("/users/me")['id']

client.patch(f'/users/{id}', json={"token": "admin"})

