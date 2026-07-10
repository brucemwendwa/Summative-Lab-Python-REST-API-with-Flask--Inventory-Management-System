import requests
import json
import sys
from typing import Optional

BASE_URL = "http://localhost:5000"


class InventoryCLI:
    """CLI interface for the Inventory Management System."""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    def print_header(self, title: str):
        """Print a formatted header."""
        print(f"\n{'='*60}")
        print(f"{title:^60}")
        print(f"{'='*60}\n")

    def print_item(self, item: dict):
        """Print a formatted inventory item."""
        print(f"ID: {item['id']}")
        print(f"Product: {item['product_name']}")
        print(f"Brand: {item['brands']}")
        print(f"Barcode: {item.get('barcode', 'N/A')}")
        print(f"Category: {item.get('category', 'N/A')}")
        print(f"Price: ${item.get('price', 0):.2f}")
        print(f"Quantity: {item.get('quantity', 0)}")
        print(f"Ingredients: {item.get('ingredients_text', 'N/A')}")
        print("-" * 60)

    def list_items(self):
        """List all inventory items."""
        try:
            response = requests.get(f"{self.base_url}/inventory")
            if response.status_code == 200:
                items = response.json()
                self.print_header("📦 All Inventory Items")
                if not items:
                    print("No items in inventory.\n")
                    return
                for item in items:
                    self.print_item(item)
                print(f"\nTotal items: {len(items)}\n")
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to the API. Make sure the server is running.")

    def get_item(self, item_id: int):
        """Get a specific inventory item."""
        try:
            response = requests.get(f"{self.base_url}/inventory/{item_id}")
            if response.status_code == 200:
                item = response.json()
                self.print_header(f"Item #{item_id}")
                self.print_item(item)
            elif response.status_code == 404:
                print(f"Error: Item with ID {item_id} not found.")
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to the API. Make sure the server is running.")

    def add_item(self):
        """Add a new inventory item."""
        self.print_header("➕ Add New Inventory Item")

        try:
            product_name = input("Product name: ").strip()
            brands = input("Brand: ").strip()
            barcode = input("Barcode (optional): ").strip() or None
            category = input("Category (default: General): ").strip() or "General"
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))
            ingredients = input("Ingredients (optional): ").strip() or "Not available"

            data = {
                "product_name": product_name,
                "brands": brands,
                "barcode": barcode,
                "category": category,
                "price": price,
                "quantity": quantity,
                "ingredients_text": ingredients,
            }

            response = requests.post(f"{self.base_url}/inventory", json=data)

            if response.status_code == 201:
                item = response.json()
                print("\n✅ Item added successfully!")
                self.print_item(item)
            elif response.status_code == 400:
                print(f"Error: {response.json().get('error', 'Invalid data')}")
            else:
                print(f"Error: {response.status_code}")
        except ValueError:
            print("Error: Invalid input. Please enter valid values.")
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to the API. Make sure the server is running.")

    def update_item(self):
        """Update an existing inventory item."""
        self.print_header("✏️  Update Inventory Item")

        try:
            item_id = int(input("Enter item ID to update: "))
            self.get_item(item_id)

            print("\nEnter new values (press Enter to skip):")
            updates = {}

            price_input = input("New price (optional): ").strip()
            if price_input:
                updates["price"] = float(price_input)

            quantity_input = input("New quantity (optional): ").strip()
            if quantity_input:
                updates["quantity"] = int(quantity_input)

            product_name = input("New product name (optional): ").strip()
            if product_name:
                updates["product_name"] = product_name

            if not updates:
                print("No updates provided.")
                return

            response = requests.patch(f"{self.base_url}/inventory/{item_id}", json=updates)

            if response.status_code == 200:
                item = response.json()
                print("\n✅ Item updated successfully!")
                self.print_item(item)
            elif response.status_code == 404:
                print(f"Error: Item with ID {item_id} not found.")
            else:
                print(f"Error: {response.status_code}")
        except ValueError:
            print("Error: Invalid input. Please enter valid values.")
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to the API. Make sure the server is running.")

    def delete_item(self):
        """Delete an inventory item."""
        self.print_header("🗑️  Delete Inventory Item")

        try:
            item_id = int(input("Enter item ID to delete: "))
            self.get_item(item_id)

            confirm = input("\nAre you sure? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("Deletion cancelled.")
                return

            response = requests.delete(f"{self.base_url}/inventory/{item_id}")

            if response.status_code == 200:
                print("✅ Item deleted successfully!")
            elif response.status_code == 404:
                print(f"Error: Item with ID {item_id} not found.")
            else:
                print(f"Error: {response.status_code}")
        except ValueError:
            print("Error: Invalid ID format.")
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to the API. Make sure the server is running.")

    def search_by_barcode(self):
        """Search for a product in OpenFoodFacts API by barcode."""
        self.print_header("🔍 Search OpenFoodFacts by Barcode")

        try:
            barcode = input("Enter barcode: ").strip()
            if not barcode:
                print("Barcode cannot be empty.")
                return

            response = requests.get(f"{self.base_url}/external-api/search/barcode/{barcode}")

            if response.status_code == 200:
                product = response.json()
                self.print_header("Product Found")
                print(f"Product: {product['product_name']}")
                print(f"Brand: {product['brands']}")
                print(f"Barcode: {product['barcode']}")
                print(f"Category: {product.get('category', 'N/A')}")
                print(f"Ingredients: {product['ingredients_text']}\n")

                add_to_inventory = input("Add this product to inventory? (yes/no): ").strip().lower()
                if add_to_inventory == "yes":
                    quantity = int(input("Quantity: "))
                    price = float(input("Price: "))
                    self.add_from_external_api(barcode, quantity, price)
            elif response.status_code == 404:
                print("Product not found in OpenFoodFacts database.")
            else:
                print(f"Error: {response.status_code}")
        except ValueError:
            print("Error: Invalid input.")
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to the API. Make sure the server is running.")

    def search_by_name(self):
        """Search for products in OpenFoodFacts API by name."""
        self.print_header("🔍 Search OpenFoodFacts by Name")

        try:
            product_name = input("Enter product name: ").strip()
            if not product_name:
                print("Product name cannot be empty.")
                return

            response = requests.get(
                f"{self.base_url}/external-api/search/name",
                params={"q": product_name}
            )

            if response.status_code == 200:
                products = response.json()
                self.print_header("Search Results")
                for idx, product in enumerate(products, 1):
                    print(f"\n{idx}. {product['product_name']} by {product['brands']}")
                    print(f"   Barcode: {product['barcode']}")
                    print(f"   Category: {product.get('category', 'N/A')}")
                    print(f"   Ingredients: {product['ingredients_text']}")

                selection = input("\nSelect a product to add (1-5) or 'skip': ").strip()
                if selection.isdigit() and 1 <= int(selection) <= len(products):
                    idx = int(selection) - 1
                    barcode = products[idx]["barcode"]
                    quantity = int(input("Quantity: "))
                    price = float(input("Price: "))
                    self.add_from_external_api(barcode, quantity, price)
                else:
                    print("Skipped.")
            elif response.status_code == 404:
                print("No products found matching your search.")
            else:
                print(f"Error: {response.status_code}")
        except ValueError:
            print("Error: Invalid input.")
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to the API. Make sure the server is running.")

    def add_from_external_api(self, barcode: str, quantity: int, price: float):
        """Add a product from external API to inventory."""
        data = {
            "quantity": quantity,
            "price": price,
        }

        try:
            response = requests.post(
                f"{self.base_url}/inventory/from-external/{barcode}",
                json=data
            )

            if response.status_code == 201:
                item = response.json()
                print("\n✅ Product added to inventory successfully!")
                self.print_item(item)
            elif response.status_code == 404:
                print("Error: Product not found in external API.")
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to the API. Make sure the server is running.")

    def show_menu(self):
        """Display the main menu."""
        self.print_header("📦 Inventory Management System")
        print("1. View all items")
        print("2. View item details")
        print("3. Add new item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Search OpenFoodFacts by barcode")
        print("7. Search OpenFoodFacts by name")
        print("8. Exit")
        print()

    def run(self):
        """Run the CLI application."""
        while True:
            self.show_menu()
            choice = input("Select an option (1-8): ").strip()

            if choice == "1":
                self.list_items()
            elif choice == "2":
                try:
                    item_id = int(input("Enter item ID: "))
                    self.get_item(item_id)
                except ValueError:
                    print("Error: Invalid ID format.")
            elif choice == "3":
                self.add_item()
            elif choice == "4":
                self.update_item()
            elif choice == "5":
                self.delete_item()
            elif choice == "6":
                self.search_by_barcode()
            elif choice == "7":
                self.search_by_name()
            elif choice == "8":
                print("\nThank you for using the Inventory Management System. Goodbye! 👋\n")
                sys.exit(0)
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    cli = InventoryCLI()
    cli.run()
