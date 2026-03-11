from flask import Flask, request, jsonify
import uuid

import logging
import json
from datetime import datetime
from flask import g

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("order-api")

from flask import g

def log_json(level, event, **kwargs):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "event": event,
        "request_id": getattr(g, "request_id", None),
        **kwargs
    }

    if level == "INFO":
        logger.info(json.dumps(log_entry))
    elif level == "WARN":
        logger.warning(json.dumps(log_entry))
    elif level == "ERROR":
        logger.error(json.dumps(log_entry))

app = Flask(__name__)

@app.before_request
def assign_request_id():
    g.request_id = str(uuid.uuid4())

# In-memory order storage
orders = {}

# Health check endpoint
@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


# Create an order
@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    order_id = str(uuid.uuid4())

    order = {
        "id": order_id,
        "item": data.get("item"),
        "price": data.get("price")
    }

    orders[order_id] = order

    log_json(
    "INFO",
    "order_created",
    order_id=order_id,
    item=order["item"],
    price=order["price"]
)


    return jsonify(order), 201
    

# Get an order
@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):

    order = orders.get(order_id)

    if not order:
        log_json(
            "WARN",
            "order_not_found",
            order_id=order_id
        )
        return jsonify({"error": "Order not found"}), 404

    log_json(
        "INFO",
        "order_retrieved",
        order_id=order_id
    )

    return jsonify(order), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)