from flask import Flask, jsonify

app = Flask(__name__)

# Dummy database for products
products = [
    {"id": 1, "name": "Laptop", "price": 1000.00},
    {"id": 2, "name": "Wireless Mouse", "price": 25.50},
    {"id": 3, "name": "Mechanical Keyboard", "price": 85.00}
]

@app.route('/products', methods=['GET'])
def get_products():
    """Retrieve all products."""
    return jsonify({"products": products}), 200

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Retrieve a single product by ID."""
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    # Product service runs on port 5001
    app.run(host='0.0.0.0', port=5001, debug=True)
