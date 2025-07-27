# backend_api.py
import json
import random
import time
import datetime
from flask import Flask, request, jsonify
from config import ORDERS_FILE, BACKEND_HOST, BACKEND_PORT

app = Flask(__name__)
backend_orders = {}  # In-memory storage for orders

def load_orders():
    """Load orders from JSON file"""
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_orders():
    """Save orders to JSON file"""
    try:
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(backend_orders, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving orders: {e}")

def generate_order_id():
    """Generate a unique order ID"""
    return f"ORD-{random.randint(1000, 9999)}-{int(time.time() % 10000)}"

def calculate_eta(items):
    """Calculate estimated delivery time based on items"""
    base_time = 15  # Base preparation time in minutes
    item_time = len(items) * 3  # 3 minutes per item
    random_factor = random.randint(-5, 10)  # Random variation
    total_eta = max(10, base_time + item_time + random_factor)  # Minimum 10 minutes
    return total_eta

@app.route('/submit-order', methods=['POST'])
def submit_order_api():
    """Backend API endpoint for order submission"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        name = data.get('name')
        items = data.get('items', [])
        
        if not name or not items:
            return jsonify({"error": "Name and items are required"}), 400
        
        # Generate order details
        order_id = generate_order_id()
        eta = calculate_eta(items)
        timestamp = datetime.datetime.now().isoformat()
        
        # Store order
        order_data = {
            "order_id": order_id,
            "name": name,
            "items": items,
            "eta_minutes": eta,
            "status": "confirmed",
            "timestamp": timestamp,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        backend_orders[order_id] = order_data
        save_orders()  # Persist to JSON
        
        return jsonify({
            "success": True,
            "order_id": order_id,
            "eta_minutes": eta,
            "message": f"تم تأكيد طلبك بنجاح! رقم الطلب: {order_id}، الوقت المتوقع: {eta} دقيقة",
            "order_details": order_data
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/orders', methods=['GET'])
def get_all_orders():
    """Get all orders"""
    return jsonify(backend_orders), 200

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get specific order by ID"""
    if order_id in backend_orders:
        return jsonify(backend_orders[order_id]), 200
    else:
        return jsonify({"error": "Order not found"}), 404

def initialize_backend():
    """Initialize the backend with existing orders"""
    global backend_orders
    backend_orders = load_orders()

def run_backend():
    """Run the Flask backend"""
    initialize_backend()
    app.run(host=BACKEND_HOST, port=BACKEND_PORT, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_backend()