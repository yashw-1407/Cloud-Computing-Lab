from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Dummy database for orders
orders = []

# Docker service names act as hostnames in the Docker Compose network
PRODUCT_SERVICE_URL = "http://product-service:5001"
PAYMENT_SERVICE_URL = "http://payment-service:5003"

@app.route('/orders', methods=['POST'])
def create_order():
    """Create a new order and coordinate with Product and Payment services."""
    data = request.get_json() or {}
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400
    
    # 1. Communicate with Product Service
    try:
        prod_response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}", timeout=5)
        if prod_response.status_code != 200:
            return jsonify({"error": f"Product verification failed: {prod_response.text}"}), prod_response.status_code
        
        product_data = prod_response.json()
        price = product_data.get('price', 0)
    except Exception as e:
        return jsonify({"error": f"Failed to connect to product-service: {str(e)}"}), 500

    # Calculate total amount
    total_amount = price * quantity

    # Create preliminary order
    order_id = len(orders) + 1
    order = {
        "order_id": order_id,
        "product_id": product_id,
        "quantity": quantity,
        "total_amount": total_amount,
        "status": "Pending Payment"
    }
    
    # 2. Communicate with Payment Service
    try:
        pay_payload = {"order_id": order_id, "amount": total_amount}
        pay_response = requests.post(f"{PAYMENT_SERVICE_URL}/pay", json=pay_payload, timeout=5)
        
        if pay_response.status_code == 200:
            payment_data = pay_response.json()
            order['status'] = "Paid"
            order['payment_info'] = payment_data.get('payment')
        else:
            order['status'] = "Payment Failed"
            return jsonify({"error": "Payment failed", "order": order}), 400
    except Exception as e:
        order['status'] = "Payment Service Unavailable"
        return jsonify({"error": f"Failed to connect to payment-service: {str(e)}", "order": order}), 500

    orders.append(order)
    return jsonify({"message": "Order completed successfully", "order": order}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    """Retrieve all orders."""
    return jsonify({"orders": orders}), 200

if __name__ == '__main__':
    # Order service runs on port 5002
    app.run(host='0.0.0.0', port=5002, debug=True)
