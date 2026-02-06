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
