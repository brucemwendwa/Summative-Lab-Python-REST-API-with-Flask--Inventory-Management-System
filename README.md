# Inventory Management System

A comprehensive REST API-based inventory management system built with Flask, featuring real-time product data integration from OpenFoodFacts API and a command-line interface for easy inventory management.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete inventory items
- **External API Integration**: Fetch product details from OpenFoodFacts API by barcode or product name
- **Flask REST API**: RESTful endpoints for programmatic access
- **CLI Interface**: User-friendly command-line tool for inventory management
- **Comprehensive Testing**: Unit tests for all endpoints and external API interactions
- **Error Handling**: Robust error handling for invalid inputs and API failures

## Project Structure

```
.
├── app.py                    # Main Flask application with all endpoints
├── cli.py                    # CLI interface for inventory management
├── external_api.py           # External API integration (OpenFoodFacts)
├── mock_database.py          # Mock database with sample data
├── test_app.py              # Unit tests for Flask endpoints
├── test_external_api.py      # Unit tests for external API functions
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository** (if using Git):
   ```bash
   git clone <repository-url>
   cd "Summative Lab: Python REST API with Flask- Inventory Management System"
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the Flask Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

### Run the CLI Application

In a new terminal (with the virtual environment activated):

```bash
python cli.py
```

Follow the interactive menu to manage your inventory.

## API Endpoints

### Inventory Management Endpoints

#### Get All Items
- **Route**: `GET /inventory`
- **Description**: Fetch all inventory items
- **Response**: 
  ```json
  [
    {
      "id": 1,
      "product_name": "Organic Almond Milk",
      "brands": "Silk",
      "barcode": "0025000537009",
      "ingredients_text": "Filtered water, almonds...",
      "quantity": 50,
      "price": 3.99,
      "category": "Beverages",
      "external_id": null
    }
  ]
  ```

#### Get Single Item
- **Route**: `GET /inventory/<id>`
- **Description**: Fetch a specific inventory item by ID
- **Parameters**: `id` (integer) - Item ID
- **Response**: Single item object (see above)
- **Error Response** (404):
  ```json
  {"error": "Item not found"}
  ```

#### Create Item
- **Route**: `POST /inventory`
- **Description**: Add a new inventory item
- **Request Body**:
  ```json
  {
    "product_name": "Product Name",
    "brands": "Brand Name",
    "barcode": "1234567890",
    "category": "Category",
    "price": 9.99,
    "quantity": 10,
    "ingredients_text": "Ingredient list"
  }
  ```
- **Required Fields**: `product_name`, `brands`, `price`, `quantity`
- **Response** (201):
  ```json
  {
    "id": 4,
    "product_name": "Product Name",
    "brands": "Brand Name",
    ...
  }
  ```
- **Error Response** (400):
  ```json
  {"error": "Missing required fields"}
  ```

#### Update Item
- **Route**: `PATCH /inventory/<id>`
- **Description**: Update an existing inventory item
- **Parameters**: `id` (integer) - Item ID
- **Request Body** (partial update):
  ```json
  {
    "price": 7.99,
    "quantity": 25
  }
  ```
- **Response** (200): Updated item object
- **Error Response** (404):
  ```json
  {"error": "Item not found"}
  ```

#### Delete Item
- **Route**: `DELETE /inventory/<id>`
- **Description**: Delete an inventory item
- **Parameters**: `id` (integer) - Item ID
- **Response** (200):
  ```json
  {"message": "Item deleted successfully"}
  ```
- **Error Response** (404):
  ```json
  {"error": "Item not found"}
  ```

### External API Endpoints

#### Search by Barcode
- **Route**: `GET /external-api/search/barcode/<barcode>`
- **Description**: Search for a product in OpenFoodFacts by barcode
- **Parameters**: `barcode` (string) - Product barcode
- **Response** (200):
  ```json
  {
    "product_name": "Product Name",
    "brands": "Brand Name",
    "barcode": "1234567890",
    "ingredients_text": "...",
    "category": "...",
    "external_id": "..."
  }
  ```
- **Error Response** (404):
  ```json
  {"error": "Product not found"}
  ```

#### Search by Name
- **Route**: `GET /external-api/search/name?q=<product_name>`
- **Description**: Search for products in OpenFoodFacts by name
- **Parameters**: `q` (string) - Product name to search for
- **Response** (200): Array of up to 5 matching products
- **Error Response** (400):
  ```json
  {"error": "Product name required"}
  ```
- **Error Response** (404):
  ```json
  {"error": "No products found"}
  ```

#### Add Product from External API
- **Route**: `POST /inventory/from-external/<barcode>`
- **Description**: Fetch a product from OpenFoodFacts and add it to inventory
- **Parameters**: `barcode` (string) - Product barcode
- **Request Body**:
  ```json
  {
    "quantity": 10,
    "price": 5.99
  }
  ```
- **Response** (201): New inventory item
- **Error Response** (404):
  ```json
  {"error": "Product not found in external API"}
  ```

### Health Check

#### Health Check
- **Route**: `GET /health`
- **Description**: Check if the API is running
- **Response** (200):
  ```json
  {"status": "healthy"}
  ```

## CLI Usage Examples

### Main Menu
When you run `python cli.py`, you'll see the main menu:

```
============================================================
                Inventory Management System
============================================================

1. View all items
2. View item details
3. Add new item
4. Update item
5. Delete item
6. Search OpenFoodFacts by barcode
7. Search OpenFoodFacts by name
8. Exit
```

### Example: View All Items
```
Select an option (1-8): 1

============================================================
                   All Inventory Items
============================================================

ID: 1
Product: Organic Almond Milk
Brand: Silk
Barcode: 0025000537009
Category: Beverages
Price: $3.99
Quantity: 50
Ingredients: Filtered water, almonds, cane sugar, calcium carbonate
```

### Example: Search and Add from OpenFoodFacts
```
Select an option (1-8): 6

============================================================
              Search OpenFoodFacts by Barcode
============================================================

Enter barcode: 0025000537009

============================================================
                    Product Found
============================================================

Product: Organic Almond Milk
Brand: Silk
Barcode: 0025000537009
Category: Beverages
Ingredients: Filtered water, almonds, cane sugar, calcium carbonate

Add this product to inventory? (yes/no): yes
Quantity: 25
Price: 4.49

✅ Product added to inventory successfully!
```

### Example: Add New Item Manually
```
Select an option (1-8): 3

============================================================
               Add New Inventory Item
============================================================

Product name: Premium Orange Juice
Brand: Tropicana
Barcode (optional): 0651159141
Category (default: General): Beverages
Price: 5.99
Quantity: 40
Ingredients (optional): 100% pure orange juice

✅ Item added successfully!
```

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest test_app.py        # Test Flask endpoints
pytest test_external_api.py  # Test external API functions
```

### Run Tests with Verbose Output
```bash
pytest -v
```

### Run Tests with Coverage Report
```bash
pytest --cov=. --cov-report=html
```

### Test Coverage

The test suite includes:

**test_app.py**:
- Health check endpoint tests
- GET endpoint tests (all items, single item)
- POST endpoint tests (create new item, validation)
- PATCH endpoint tests (update item, partial updates)
- DELETE endpoint tests (delete item, cascade)
- External API endpoint tests
- Complete CRUD workflow tests

**test_external_api.py**:
- Successful product fetch by barcode
- Failed product fetch scenarios
- Network error handling
- Timeout error handling
- HTTP error handling
- Product search by name
- Search result limiting
- Missing field handling

## Example API Requests

### Using cURL

```bash
# Get all items
curl http://localhost:5000/inventory

# Get single item
curl http://localhost:5000/inventory/1

# Create new item
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Milk",
    "brands": "Local Dairy",
    "price": 3.99,
    "quantity": 50
  }'

# Update item
curl -X PATCH http://localhost:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 4.49,
    "quantity": 75
  }'

# Delete item
curl -X DELETE http://localhost:5000/inventory/1

# Search by barcode
curl http://localhost:5000/external-api/search/barcode/0025000537009

# Search by name
curl "http://localhost:5000/external-api/search/name?q=almond%20milk"

# Add from external API
curl -X POST http://localhost:5000/inventory/from-external/0025000537009 \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 20,
    "price": 4.49
  }'
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:5000"

# Get all items
response = requests.get(f"{BASE_URL}/inventory")
items = response.json()

# Create new item
new_item = {
    "product_name": "Bread",
    "brands": "Local Bakery",
    "price": 3.49,
    "quantity": 30
}
response = requests.post(f"{BASE_URL}/inventory", json=new_item)

# Update item
updates = {"price": 3.99, "quantity": 50}
response = requests.patch(f"{BASE_URL}/inventory/1", json=updates)

# Delete item
response = requests.delete(f"{BASE_URL}/inventory/1")
```

## Mock Database Structure

The mock database (`mock_database.py`) contains sample inventory items with the following structure:

```python
{
    "id": 1,                                          # Unique identifier
    "product_name": "Organic Almond Milk",           # Product name
    "brands": "Silk",                                 # Brand name
    "barcode": "0025000537009",                      # Product barcode
    "ingredients_text": "Filtered water, almonds...", # Ingredients
    "quantity": 50,                                   # Stock quantity
    "price": 3.99,                                    # Unit price
    "category": "Beverages",                          # Product category
    "external_id": None                               # External API ID
}
```

## OpenFoodFacts API Integration

The system integrates with the OpenFoodFacts API to:

1. **Fetch product details by barcode**: Retrieves comprehensive product information using a barcode
2. **Search for products by name**: Allows users to find products by typing their name
3. **Supplement inventory data**: Enhances stored inventory with real-world product data

The external API module (`external_api.py`) handles all API communication with proper error handling and logging.

## Error Handling

The system implements comprehensive error handling:

- **Invalid input validation**: Checks for missing or invalid fields
- **HTTP error responses**: Appropriate status codes (200, 201, 400, 404)
- **Network error handling**: Gracefully handles API timeouts and connection failures
- **User-friendly error messages**: Clear error messages in the CLI

## Git Repository Management

This project uses Git for version control:

```bash
# Initialize repository
git init

# Create feature branches
git checkout -b feature/api-endpoints
git checkout -b feature/external-api
git checkout -b feature/cli-interface

# Stage and commit changes
git add .
git commit -m "Add API endpoints"

# Merge branches
git checkout main
git merge feature/api-endpoints
```

## Development Notes

### Adding New Features

1. **New Endpoint**: Add route to `app.py`
2. **New Database Field**: Update `mock_database.py` structure
3. **New External API Function**: Add to `external_api.py`
4. **New CLI Command**: Add to `cli.py`
5. **Tests**: Add comprehensive tests to `test_app.py` or `test_external_api.py`

### Best Practices

- Always add tests for new features
- Use meaningful variable and function names
- Keep error handling comprehensive
- Document API changes in README.md
- Commit frequently with clear messages

## Troubleshooting

### Port 5000 Already in Use
```bash
# Find and kill the process using port 5000
lsof -i :5000
kill -9 <PID>

# Or use a different port by editing app.py
app.run(debug=True, host="0.0.0.0", port=5001)
```

### Connection Error in CLI
Make sure the Flask server is running in a separate terminal with `python app.py`

### OpenFoodFacts API Timeout
The API might be temporarily unavailable. Try again in a few moments.

## Performance Optimization

- The mock database uses in-memory storage for fast access
- External API calls include 5-second timeouts to prevent hanging
- The CLI provides immediate feedback for all operations

## Future Enhancements

- Persistent database (SQLite, PostgreSQL)
- User authentication and authorization
- Advanced search filters
- Inventory alerts for low stock
- Barcode scanning with hardware devices
- Export/Import functionality (CSV, JSON)
- Analytics and reporting dashboard
- Multi-user support with audit logs

## License

This project is created for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the test files for usage examples
3. Check the API documentation above
