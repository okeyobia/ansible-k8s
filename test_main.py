import pytest
from fastapi.testclient import TestClient
from main import app, Item


client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint"""

    def test_root_returns_hello_message(self):
        """Test that root endpoint returns correct message"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, World!"}


class TestHealthEndpoint:
    """Tests for the health check endpoint"""

    def test_health_check_returns_healthy(self):
        """Test that health endpoint returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestItemsGetEndpoint:
    """Tests for reading items"""

    def test_read_item_without_query(self):
        """Test reading an item without query parameter"""
        response = client.get("/items/1")
        assert response.status_code == 200
        data = response.json()
        assert data["item_id"] == 1
        assert data["q"] is None

    def test_read_item_with_query(self):
        """Test reading an item with query parameter"""
        response = client.get("/items/42?q=search_term")
        assert response.status_code == 200
        data = response.json()
        assert data["item_id"] == 42
        assert data["q"] == "search_term"

    def test_read_item_with_multiple_items(self):
        """Test reading different items"""
        for item_id in [1, 100, 999]:
            response = client.get(f"/items/{item_id}")
            assert response.status_code == 200
            assert response.json()["item_id"] == item_id


class TestItemsPostEndpoint:
    """Tests for creating items"""

    def test_create_item_with_all_fields(self):
        """Test creating an item with all fields"""
        item_data = {
            "name": "Widget",
            "description": "A useful widget",
            "price": 9.99,
            "tax": 0.99,
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Widget"
        assert data["description"] == "A useful widget"
        assert data["price"] == 9.99
        assert data["tax"] == 0.99

    def test_create_item_without_optional_fields(self):
        """Test creating an item with only required fields"""
        item_data = {
            "name": "Gadget",
            "price": 19.99,
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Gadget"
        assert data["price"] == 19.99
        assert data["description"] is None
        assert data["tax"] is None

    def test_create_item_missing_required_field(self):
        """Test creating an item without required name field"""
        item_data = {
            "price": 9.99,
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 422  # Unprocessable Entity

    def test_create_item_missing_price(self):
        """Test creating an item without required price field"""
        item_data = {
            "name": "Widget",
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 422  # Unprocessable Entity

    def test_create_item_invalid_price_type(self):
        """Test creating an item with invalid price type"""
        item_data = {
            "name": "Widget",
            "price": "not_a_number",
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 422  # Unprocessable Entity

    def test_create_multiple_items(self):
        """Test creating multiple items"""
        items = [
            {"name": "Item 1", "price": 10.0},
            {"name": "Item 2", "price": 20.0, "description": "Second item"},
            {"name": "Item 3", "price": 30.0, "tax": 3.0},
        ]
        for item_data in items:
            response = client.post("/items/", json=item_data)
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == item_data["name"]
            assert data["price"] == item_data["price"]


class TestApiSchema:
    """Tests for API documentation endpoints"""

    def test_openapi_schema_available(self):
        """Test that OpenAPI schema is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema

    def test_swagger_ui_available(self):
        """Test that Swagger UI documentation is available"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()

    def test_redoc_available(self):
        """Test that ReDoc documentation is available"""
        response = client.get("/redoc")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
