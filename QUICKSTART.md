# Quick Start Guide

Get the Inventory Management System up and running in 5 minutes!

## Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

## Installation (1 minute)

```bash
# Navigate to the project directory
cd "Summative Lab: Python REST API with Flask- Inventory Management System"

# Create a virtual environment (recommended)
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Project

### Option 1: Use the CLI Interface (Easiest)

**Terminal 1 - Start the API server:**
```bash
python3 app.py
```
You should see:
```
 * Running on http://127.0.0.1:5000
```

**Terminal 2 - Run the CLI:**
```bash
python3 cli.py
```

You'll see the interactive menu:
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

### Option 2: Use curl/API Directly

**Start the server:**
```bash
python3 app.py
```

**In another terminal, test the API:**

```bash
# Get all items
curl http://localhost:5000/inventory

# Get a single item
curl http://localhost:5000/inventory/1

# Create a new item
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Fresh Milk",
    "brands": "Local Dairy",
    "price": 3.99,
    "quantity": 50
  }'

# Update an item
curl -X PATCH http://localhost:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 4.49}'

# Delete an item
curl -X DELETE http://localhost:5000/inventory/1

# Search OpenFoodFacts by barcode
curl http://localhost:5000/external-api/search/barcode/0025000537009

# Search OpenFoodFacts by name
curl "http://localhost:5000/external-api/search/name?q=almond%20milk"
```

## Run Tests

```bash
# Run all tests
pytest -v

# Run a specific test file
pytest test_app.py -v

# Run tests with coverage
pytest --cov=. --cov-report=html
```

**Expected Output:**
```
33 passed in 0.87s
```

## Sample Inventory Items

The system comes with 3 sample items:

1. **Organic Almond Milk** (Silk)
   - Price: $3.99
   - Quantity: 50
   - Barcode: 0025000537009

2. **Whole Wheat Bread** (Dave's Killer Bread)
   - Price: $4.99
   - Quantity: 30
   - Barcode: 0075450100807

3. **Greek Yogurt** (Fage)
   - Price: $5.49
   - Quantity: 45
   - Barcode: 0070169040017

## Common Tasks

### Add a Product from OpenFoodFacts by Barcode

**Via CLI:**
1. Run `python3 cli.py`
2. Press `6` for "Search OpenFoodFacts by barcode"
3. Enter the barcode (e.g., `0025000537009`)
4. Choose "yes" to add to inventory
5. Enter quantity and price

**Via API:**
```bash
curl -X POST http://localhost:5000/inventory/from-external/0025000537009 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 20, "price": 4.49}'
```

### Search for Products by Name

**Via CLI:**
1. Run `python3 cli.py`
2. Press `7` for "Search OpenFoodFacts by name"
3. Enter product name (e.g., `milk`)
4. Select from results
5. Choose "yes" to add and enter quantity/price

**Via API:**
```bash
curl "http://localhost:5000/external-api/search/name?q=milk"
```

### View All Inventory

**Via CLI:**
1. Run `python3 cli.py`
2. Press `1` for "View all items"

**Via API:**
```bash
curl http://localhost:5000/inventory | python3 -m json.tool
```

## Troubleshooting

### Port 5000 is already in use
```bash
# Find the process using port 5000
lsof -i :5000

# Kill the process (replace PID with actual ID)
kill -9 <PID>
```

### Virtual environment not activated
Make sure you see `(venv)` in your terminal prompt before running commands

### OpenFoodFacts API timeouts
The API is occasionally slow. Try again in a few moments.

### Import errors
Make sure you installed requirements:
```bash
pip install -r requirements.txt
```

## Project Files at a Glance

| File | Purpose |
|------|---------|
| `app.py` | Flask API with 9 endpoints |
| `cli.py` | Interactive CLI interface |
| `external_api.py` | OpenFoodFacts API integration |
| `mock_database.py` | Sample inventory data |
| `test_app.py` | 22 API endpoint tests |
| `test_external_api.py` | 11 external API tests |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |

## What's Next?

- **Read the full README.md** for detailed API documentation
- **Check PROJECT_SUMMARY.md** for implementation details
- **Review the code** in `app.py`, `cli.py`, and `external_api.py`
- **Run tests** with `pytest -v` to see all test coverage
- **Explore the OpenFoodFacts API** at https://world.openfoodfacts.org

## Support

For detailed information, see:
- `README.md` - Complete API documentation with examples
- `PROJECT_SUMMARY.md` - Rubric compliance and architecture details
- Test files for usage examples

---

**Happy inventory managing! 📦**
