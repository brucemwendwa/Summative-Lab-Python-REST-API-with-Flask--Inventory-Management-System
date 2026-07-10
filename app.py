from flask import Flask, request, jsonify
from mock_database import inventory_db, next_id
import mock_database
from external_api import fetch_product_by_barcode, fetch_product_by_name
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/inventory", methods=["GET"])
def get_all_items():
    """Fetch all inventory items."""
    return jsonify(inventory_db), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """Fetch a single inventory item by ID."""
    item = next((item for item in inventory_db if item["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404


@app.route("/inventory", methods=["POST"])
def create_item():
    """Create a new inventory item."""
    data = request.get_json()

    if not data or not all(k in data for k in ["product_name", "brands", "price", "quantity"]):
        return jsonify({"error": "Missing required fields"}), 400

    new_item = {
        "id": mock_database.next_id,
        "product_name": data.get("product_name"),
        "brands": data.get("brands"),
        "barcode": data.get("barcode", ""),
        "ingredients_text": data.get("ingredients_text", "Not available"),
        "quantity": data.get("quantity", 0),
        "price": data.get("price", 0.0),
        "category": data.get("category", "General"),
        "external_id": data.get("external_id"),
    }

    inventory_db.append(new_item)
    mock_database.next_id += 1

    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    """Update an existing inventory item."""
    item = next((item for item in inventory_db if item["id"] == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    item.update({k: v for k, v in data.items() if k in item})

    return jsonify(item), 200


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Delete an inventory item."""
    global inventory_db
    original_length = len(inventory_db)
    inventory_db = [item for item in inventory_db if item["id"] != item_id]

    if len(inventory_db) == original_length:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"message": "Item deleted successfully"}), 200


@app.route("/external-api/search/barcode/<barcode>", methods=["GET"])
def search_by_barcode(barcode):
    """Search for a product by barcode in OpenFoodFacts API."""
    result = fetch_product_by_barcode(barcode)

    if result:
        return jsonify(result), 200

    return jsonify({"error": "Product not found"}), 404


@app.route("/external-api/search/name", methods=["GET"])
def search_by_name():
    """Search for a product by name in OpenFoodFacts API."""
    product_name = request.args.get("q")

    if not product_name:
        return jsonify({"error": "Product name required"}), 400

    results = fetch_product_by_name(product_name)

    if results:
        return jsonify(results), 200

    return jsonify({"error": "No products found"}), 404


@app.route("/inventory/from-external/<barcode>", methods=["POST"])
def add_from_external_api(barcode):
    """Fetch product from external API and add it to inventory."""
    product_data = fetch_product_by_barcode(barcode)

    if not product_data:
        return jsonify({"error": "Product not found in external API"}), 404

    data = request.get_json() or {}
    new_item = {
        "id": mock_database.next_id,
        "product_name": product_data["product_name"],
        "brands": product_data["brands"],
        "barcode": barcode,
        "ingredients_text": product_data["ingredients_text"],
        "quantity": data.get("quantity", 0),
        "price": data.get("price", 0.0),
        "category": product_data.get("category", "General"),
        "external_id": product_data.get("external_id"),
    }

    inventory_db.append(new_item)
    mock_database.next_id += 1

    return jsonify(new_item), 201


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
