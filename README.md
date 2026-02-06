# Simple FastAPI App

A minimal FastAPI application built with `uv` as the Python package manager.

## Prerequisites

- Python 3.8 or higher
- `uv` installed ([Installation guide](https://docs.astral.sh/uv/getting-started/installation/))

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Run the application

```bash
uv run main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /items/{item_id}` - Get an item by ID (with optional query parameter `q`)
- `POST /items/` - Create a new item

## Interactive API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Alternative: Using uvicorn directly

```bash
uv run uvicorn main:app --reload
```

The `--reload` flag enables auto-reload on file changes (useful for development).

## Running Tests

First, install dev dependencies:

```bash
uv sync --extra dev
```

Then run the tests:

```bash
uv run pytest test_main.py -v
```

### Test Coverage

The test suite includes 14 tests covering:

- **Root endpoint** - Verifies the welcome message
- **Health check endpoint** - Confirms the server is healthy
- **Read items** - Tests GET /items/{id} with and without query parameters
- **Create items** - Tests POST /items/ with various payload combinations
- **Schema validation** - Tests OpenAPI schema, Swagger UI, and ReDoc endpoints

Tests validate:
- Correct HTTP status codes
- Response data structures
- Required vs optional parameters
- Invalid input handling

## Project Structure

```
.
├── main.py          # FastAPI application
├── pyproject.toml   # Project configuration (uv)
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

## Example Requests

### GET /
```bash
curl http://localhost:8000/
```

### GET /items/1
```bash
curl "http://localhost:8000/items/1?q=test"
```

### POST /items/
```bash
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget", "price": 9.99, "description": "A useful widget"}'
```

## Kubernetes Deployment (Minikube)

### Prerequisites

- Minikube installed and running
- kubectl installed
- Docker image built

### 1. Build the Docker image for Minikube

First, set up your shell to use Minikube's Docker daemon:

```bash
eval $(minikube docker-env)
```

Then build the image:

```bash
docker build -t fastapi-app:latest .
```

### 2. Deploy to Minikube

Create the namespace and deploy the application:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Or apply all at once:

```bash
kubectl apply -f k8s/
```

### 3. Check deployment status

```bash
# Check pod status
kubectl get pods -n fastapi

# Check service
kubectl get svc -n fastapi

# View deployment details
kubectl describe deployment fastapi-app -n fastapi
```

### 4. Access the application

Using the Minikube service command:

```bash
minikube service fastapi-app -n fastapi
```

This will automatically open the service in your browser.

**API endpoints:**
- `http://<minikube-ip>:30000/` - Root endpoint
- `http://<minikube-ip>:30000/docs` - Swagger UI
- `http://<minikube-ip>:30000/health` - Health check

### 5. View logs

```bash
# View logs from all pods
kubectl logs -n fastapi -l app=fastapi-app --tail=50 -f

# View logs from specific pod
kubectl logs -n fastapi <pod-name>
```

### 6. Clean up

```bash
# Remove all resources
kubectl delete -f k8s/

# Or delete the entire namespace
kubectl delete namespace fastapi
```

### Troubleshooting

**Image not found error:**
- Ensure you've set `eval $(minikube docker-env)` before building
- Rebuild the image: `docker build -t fastapi-app:latest .`

**Pod not starting:**
- Check pod logs: `kubectl logs -n fastapi <pod-name>`
- Check pod events: `kubectl describe pod -n fastapi <pod-name>`

**Service not accessible:**
- Verify service is created: `kubectl get svc -n fastapi`
- Check endpoints: `kubectl get endpoints -n fastapi`

## Docker Deployment

### Build the Docker image

```bash
docker build -t fastapi-app:latest .
```

### Run the container

```bash
docker run -p 8000:8000 fastapi-app:latest
```

The API will be available at `http://localhost:8000`

### Using Docker Compose

For a simpler setup, use Docker Compose:

```bash
docker-compose up --build
```

To stop and remove the container:

```bash
docker-compose down
```

### Docker Features

- **Multi-stage build** - Reduces final image size
- **Non-root user** - Runs with unprivileged `appuser` for security
- **Health checks** - Built-in health check endpoint monitoring
- **Environment variables** - `PYTHONUNBUFFERED` for real-time logs
- **Volume ready** - Can be extended with volume mounts for data persistence

## License

MIT
