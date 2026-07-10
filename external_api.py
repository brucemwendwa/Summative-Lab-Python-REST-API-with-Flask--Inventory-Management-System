import requests
import logging

logger = logging.getLogger(__name__)

# OpenFoodFacts Official API Reference:
# https://openfoodfacts.github.io/openfoodfacts-server/api/
OPENFOODSFACTS_URL = "https://world.openfoodfacts.org/api/v0/product"
OPENFOODSFACTS_SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"


def fetch_product_by_barcode(barcode):
    """
    Fetch product data from OpenFoodFacts API using a barcode.

    API Reference: https://openfoodfacts.github.io/openfoodfacts-server/api/
    Endpoint: GET /api/v0/product/{barcode}.json

    Args:
        barcode (str): The product barcode (EAN, UPC, etc.)

    Returns:
        dict: Product data if found, None otherwise
    """
    try:
        url = f"{OPENFOODSFACTS_URL}/{barcode}.json"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()
        if data.get("status") == 1 and "product" in data:
            product = data["product"]
            return {
                "product_name": product.get("product_name", "Unknown"),
                "brands": product.get("brands", "Unknown"),
                "barcode": barcode,
                "ingredients_text": product.get("ingredients_text", "Not available"),
                "category": product.get("categories", "Unknown"),
                "external_id": data.get("code"),
            }
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching product from OpenFoodFacts: {e}")
        return None


def fetch_product_by_name(product_name):
    """
    Search for a product by name in OpenFoodFacts API.

    API Reference: https://openfoodfacts.github.io/openfoodfacts-server/api/
    Endpoint: GET /cgi/search.pl (Search API)

    Args:
        product_name (str): The product name to search for

    Returns:
        list: List of matching products (max 5 results), empty list otherwise
    """
    try:
        url = OPENFOODSFACTS_SEARCH_URL
        params = {
            "search_terms": product_name,
            "json": 1,
            "pageSize": 5,
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()
        products = []

        if data.get("products"):
            for product in data["products"][:5]:
                products.append({
                    "product_name": product.get("product_name", "Unknown"),
                    "brands": product.get("brands", "Unknown"),
                    "barcode": product.get("code", "Unknown"),
                    "ingredients_text": product.get("ingredients_text", "Not available"),
                    "category": product.get("categories", "Unknown"),
                    "external_id": product.get("code"),
                })

        return products
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching products in OpenFoodFacts: {e}")
        return []
