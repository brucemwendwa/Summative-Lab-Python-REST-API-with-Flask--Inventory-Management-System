import pytest
import json
from unittest.mock import patch, MagicMock
from app import app
from mock_database import inventory_db
import mock_database


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def reset_db():
    """Reset the database before and after each test."""
    original_db = [item.copy() for item in inventory_db]
    original_next_id = mock_database.next_id
    inventory_db.clear()
    inventory_db.extend([item.copy() for item in original_db])
    yield
    inventory_db.clear()
    inventory_db.extend([item.copy() for item in original_db])
    mock_database.next_id = original_next_id


class TestHealthCheck:
    """Test suite for health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json["status"] == "healthy"


class TestGetEndpoints:
    """Test suite for GET endpoints."""

    def test_get_all_items(self, client, reset_db):
        """Test fetching all inventory items."""
        response = client.get("/inventory")
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) >= 0

    def test_get_single_item_success(self, client, reset_db):
        """Test fetching a single item that exists."""
        response = client.get("/inventory/1")
        assert response.status_code == 200
        assert response.json["id"] == 1

    def test_get_single_item_not_found(self, client, reset_db):
        """Test fetching a single item that doesn't exist."""
        response = client.get("/inventory/9999")
        assert response.status_code == 404
        assert "error" in response.json


class TestCreateEndpoint:
    """Test suite for POST endpoints."""

    def test_create_item_success(self, client, reset_db):
        """Test creating a new inventory item."""
        new_item = {
            "product_name": "Test Product",
            "brands": "Test Brand",
            "price": 9.99,
            "quantity": 10,
        }
        response = client.post("/inventory", json=new_item)
        assert response.status_code == 201
        assert response.json["product_name"] == "Test Product"
        assert response.json["brands"] == "Test Brand"

    def test_create_item_missing_fields(self, client, reset_db):
        """Test creating an item with missing required fields."""
        incomplete_item = {
            "product_name": "Test Product",
            # Missing brands, price, quantity
        }
        response = client.post("/inventory", json=incomplete_item)
        assert response.status_code == 400
        assert "error" in response.json

    def test_create_item_empty_body(self, client, reset_db):
        """Test creating an item with empty request body."""
        response = client.post("/inventory", json={})
        assert response.status_code == 400
        assert "error" in response.json


class TestUpdateEndpoint:
    """Test suite for PATCH endpoints."""

    def test_update_item_success(self, client, reset_db):
        """Test updating an existing item."""
        updates = {
            "price": 7.99,
            "quantity": 25,
        }
        response = client.patch("/inventory/1", json=updates)
        assert response.status_code == 200
        assert response.json["price"] == 7.99
        assert response.json["quantity"] == 25

    def test_update_item_not_found(self, client, reset_db):
        """Test updating a non-existent item."""
        updates = {"price": 9.99}
        response = client.patch("/inventory/9999", json=updates)
        assert response.status_code == 404
        assert "error" in response.json

    def test_update_item_empty_body(self, client, reset_db):
        """Test updating an item with empty body."""
        response = client.patch("/inventory/1", json={})
        assert response.status_code == 400
        assert "error" in response.json

    def test_update_single_field(self, client, reset_db):
        """Test updating a single field."""
        response = client.patch("/inventory/1", json={"price": 15.99})
        assert response.status_code == 200
        assert response.json["price"] == 15.99
        assert response.json["product_name"] == inventory_db[0]["product_name"]


class TestDeleteEndpoint:
    """Test suite for DELETE endpoints."""

    def test_delete_item_success(self, client, reset_db):
        """Test deleting an existing item."""
        initial_count = len(inventory_db)
        response = client.delete("/inventory/1")
        assert response.status_code == 200
        assert len(inventory_db) == initial_count - 1

    def test_delete_item_not_found(self, client, reset_db):
        """Test deleting a non-existent item."""
        response = client.delete("/inventory/9999")
        assert response.status_code == 404
        assert "error" in response.json

    def test_delete_multiple_items(self, client, reset_db):
        """Test deleting multiple items."""
        initial_count = len(inventory_db)
        client.delete("/inventory/1")
        client.delete("/inventory/2")
        assert len(inventory_db) == initial_count - 2


class TestExternalAPIEndpoints:
    """Test suite for external API endpoints."""

    @patch("app.fetch_product_by_barcode")
    def test_search_by_barcode_success(self, mock_fetch, client, reset_db):
        """Test searching for a product by barcode."""
        mock_product = {
            "product_name": "Mock Product",
            "brands": "Mock Brand",
            "barcode": "123456789",
            "ingredients_text": "Test ingredients",
            "external_id": "mock_id",
        }
        mock_fetch.return_value = mock_product

        response = client.get("/external-api/search/barcode/123456789")
        assert response.status_code == 200
        assert response.json["product_name"] == "Mock Product"

    @patch("app.fetch_product_by_barcode")
    def test_search_by_barcode_not_found(self, mock_fetch, client, reset_db):
        """Test searching for a barcode that doesn't exist."""
        mock_fetch.return_value = None

        response = client.get("/external-api/search/barcode/999999999")
        assert response.status_code == 404
        assert "error" in response.json

    @patch("app.fetch_product_by_name")
    def test_search_by_name_success(self, mock_search, client, reset_db):
        """Test searching for products by name."""
        mock_products = [
            {
                "product_name": "Milk 1",
                "brands": "Brand 1",
                "barcode": "111",
                "ingredients_text": "Ingredients 1",
                "external_id": "id1",
            },
        ]
        mock_search.return_value = mock_products

        response = client.get("/external-api/search/name?q=milk")
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1

    @patch("app.fetch_product_by_name")
    def test_search_by_name_no_query(self, mock_search, client, reset_db):
        """Test searching without a query parameter."""
        response = client.get("/external-api/search/name")
        assert response.status_code == 400
        assert "error" in response.json

    @patch("app.fetch_product_by_name")
    def test_search_by_name_not_found(self, mock_search, client, reset_db):
        """Test searching for a name that doesn't exist."""
        mock_search.return_value = []

        response = client.get("/external-api/search/name?q=nonexistent")
        assert response.status_code == 404
        assert "error" in response.json


class TestAddFromExternalAPI:
    """Test suite for adding items from external API."""

    @patch("app.fetch_product_by_barcode")
    def test_add_from_external_api_success(self, mock_fetch, client, reset_db):
        """Test adding a product from external API."""
        mock_product = {
            "product_name": "New Product",
            "brands": "New Brand",
            "barcode": "123456789",
            "ingredients_text": "Test ingredients",
            "category": "Beverages",
            "external_id": "mock_id",
        }
        mock_fetch.return_value = mock_product

        data = {
            "quantity": 20,
            "price": 5.99,
        }

        initial_count = len(inventory_db)
        response = client.post("/inventory/from-external/123456789", json=data)
        assert response.status_code == 201
        assert response.json["product_name"] == "New Product"
        assert response.json["quantity"] == 20
        assert len(inventory_db) == initial_count + 1

    @patch("app.fetch_product_by_barcode")
    def test_add_from_external_api_not_found(self, mock_fetch, client, reset_db):
        """Test adding a product that doesn't exist in external API."""
        mock_fetch.return_value = None

        response = client.post("/inventory/from-external/999999999", json={})
        assert response.status_code == 404
        assert "error" in response.json


class TestCRUDWorkflow:
    """Test suite for complete CRUD workflows."""

    def test_create_read_update_delete_workflow(self, client, reset_db):
        """Test a complete CRUD workflow."""
        # Create
        new_item = {
            "product_name": "CRUD Test Product",
            "brands": "CRUD Test Brand",
            "price": 19.99,
            "quantity": 50,
        }
        create_response = client.post("/inventory", json=new_item)
        assert create_response.status_code == 201
        item_id = create_response.json["id"]

        # Read
        read_response = client.get(f"/inventory/{item_id}")
        assert read_response.status_code == 200
        assert read_response.json["product_name"] == "CRUD Test Product"

        # Update
        updates = {"price": 14.99, "quantity": 75}
        update_response = client.patch(f"/inventory/{item_id}", json=updates)
        assert update_response.status_code == 200
        assert update_response.json["price"] == 14.99

        # Delete
        delete_response = client.delete(f"/inventory/{item_id}")
        assert delete_response.status_code == 200

        # Verify deletion
        get_response = client.get(f"/inventory/{item_id}")
        assert get_response.status_code == 404
