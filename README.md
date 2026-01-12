# codex-workspace

## Authentication (JWT)

### Environment

Set `SECRET_KEY` (required) and optionally `ACCESS_TOKEN_EXPIRE_MINUTES` (defaults to 30).

```
SECRET_KEY=your-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Register

```
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"strongpassword"}'
```

### Login

```
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"strongpassword"}'
```

### Using the JWT

```
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"strongpassword"}' | jq -r '.access_token')

auth_header="Authorization: Bearer ${TOKEN}"
# Use ${auth_header} with protected endpoints.
```
