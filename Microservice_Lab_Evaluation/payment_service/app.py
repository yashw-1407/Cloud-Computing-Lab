from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy database for payments
payments = []

@app.route('/pay', methods=['POST'])
def process_payment():
    """Process a payment for an order."""
    data = request.get_json() or {}
    order_id = data.get('order_id')
    amount = data.get('amount')
    
    if not order_id or not amount:
        return jsonify({"error": "order_id and amount are required"}), 400
        
    payment = {
        "payment_id": len(payments) + 1,
        "order_id": order_id,
        "amount": amount,
        "status": "Success"
    }
    payments.append(payment)
    return jsonify({"message": "Payment processed successfully", "payment": payment}), 200

if __name__ == '__main__':
    # Payment service runs on port 5003
    app.run(host='0.0.0.0', port=5003, debug=True)
