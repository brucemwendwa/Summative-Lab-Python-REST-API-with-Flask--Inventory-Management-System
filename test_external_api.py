import pytest
from unittest.mock import patch, MagicMock
from external_api import fetch_product_by_barcode, fetch_product_by_name


class TestFetchProductByBarcode:
    """Test suite for fetch_product_by_barcode function."""

    @patch("external_api.requests.get")
    def test_fetch_product_success(self, mock_get):
        """Test successfully fetching a product by barcode."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 1,
            "code": "123456789",
            "product": {
                "product_name": "Test Product",
                "brands": "Test Brand",
                "ingredients_text": "Test ingredients",
                "categories": "Beverages",
            },
        }
        mock_get.return_value = mock_response

        result = fetch_product_by_barcode("123456789")

        assert result is not None
        assert result["product_name"] == "Test Product"
        assert result["brands"] == "Test Brand"
        assert result["barcode"] == "123456789"

    @patch("external_api.requests.get")
    def test_fetch_product_not_found(self, mock_get):
        """Test fetching a product that doesn't exist."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 0,
            "product": None,
        }
        mock_get.return_value = mock_response

        result = fetch_product_by_barcode("999999999")

        assert result is None

    @patch("external_api.requests.get")
    def test_fetch_product_network_error(self, mock_get):
        """Test handling of network errors."""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        result = fetch_product_by_barcode("123456789")

        assert result is None

    @patch("external_api.requests.get")
    def test_fetch_product_timeout(self, mock_get):
        """Test handling of timeout errors."""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")

        result = fetch_product_by_barcode("123456789")

        assert result is None

    @patch("external_api.requests.get")
    def test_fetch_product_http_error(self, mock_get):
        """Test handling of HTTP errors."""
        import requests
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        result = fetch_product_by_barcode("123456789")

        assert result is None


class TestFetchProductByName:
    """Test suite for fetch_product_by_name function."""

    @patch("external_api.requests.get")
    def test_search_product_success(self, mock_get):
        """Test successfully searching for products by name."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "products": [
                {
                    "product_name": "Almond Milk",
                    "brands": "Silk",
                    "code": "123456789",
                    "ingredients_text": "Water, almonds",
                    "categories": "Beverages",
                },
                {
                    "product_name": "Almond Milk 2",
                    "brands": "Blue Diamond",
                    "code": "987654321",
                    "ingredients_text": "Water, almonds, calcium",
                    "categories": "Beverages",
                },
            ]
        }
        mock_get.return_value = mock_response

        results = fetch_product_by_name("almond milk")

        assert len(results) == 2
        assert results[0]["product_name"] == "Almond Milk"
        assert results[1]["product_name"] == "Almond Milk 2"

    @patch("external_api.requests.get")
    def test_search_product_no_results(self, mock_get):
        """Test searching for a product with no results."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "products": []
        }
        mock_get.return_value = mock_response

        results = fetch_product_by_name("nonexistent product")

        assert results == []

    @patch("external_api.requests.get")
    def test_search_product_network_error(self, mock_get):
        """Test handling of network errors during search."""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        results = fetch_product_by_name("milk")

        assert results == []

    @patch("external_api.requests.get")
    def test_search_product_timeout(self, mock_get):
        """Test handling of timeout errors during search."""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")

        results = fetch_product_by_name("milk")

        assert results == []

    @patch("external_api.requests.get")
    def test_search_product_multiple_results_limited(self, mock_get):
        """Test that search results are limited to 5 items."""
        products_list = [
            {
                "product_name": f"Product {i}",
                "brands": f"Brand {i}",
                "code": str(i),
                "ingredients_text": f"Ingredients {i}",
                "categories": f"Category {i}",
            }
            for i in range(10)
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "products": products_list
        }
        mock_get.return_value = mock_response

        results = fetch_product_by_name("test")

        assert len(results) == 5

    @patch("external_api.requests.get")
    def test_search_product_missing_fields(self, mock_get):
        """Test handling of products with missing fields."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "products": [
                {
                    "product_name": "Product with missing brand",
                    # Missing brands field
                    "code": "123",
                },
            ]
        }
        mock_get.return_value = mock_response

        results = fetch_product_by_name("test")

        assert len(results) == 1
        assert results[0]["brands"] == "Unknown"
