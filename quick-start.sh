ACCESS_TOKEN=$(curl -ks -X POST $1:8055/auth/login -H "Content-Type: application/json" -d '{"email": "admin@example.com", "password": "password"}' | cut -d '"' -f6)
while [ -z "$ACCESS_TOKEN" ]
do
    ACCESS_TOKEN=$(curl -ks -X POST $1:8055/auth/login -H "Content-Type: application/json" -d '{"email": "admin@example.com", "password": "password"}' | cut -d '"' -f6)
done
DEFAULT_USER_ID=$(curl -ks -H "Authorization: Bearer $ACCESS_TOKEN" $1:8055/users/me | jq .data.id | cut -d '"' -f2)
curl -X PATCH $1:8055/users/$DEFAULT_USER_ID -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"first_name": "Admin", "last_name": "User", "token": "admin", "theme": "dark"}'