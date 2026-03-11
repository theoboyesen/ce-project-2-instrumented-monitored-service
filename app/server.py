from flask import Flask, request, jsonify, g
import uuid
import logging
import json
from datetime import datetime
import time

# Logging setup
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

file_handler = logging.FileHandler("/var/log/order-api.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


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


# Create Flask app
app = Flask(__name__)


# Assign request ID
@app.before_request
def assign_request_id():
    g.request_id = str(uuid.uuid4())


# Start latency timer
@app.before_request
def start_timer():
    g.start_time = time.time()


# Log request latency
@app.after_request
def log_request_latency(response):
    duration_ms = ((time.time() - g.start_time) * 1000, 1)

    log_json(
        "INFO",
        "request_completed",
        path=request.path,
        latency_ms=duration_ms
    )

    return response


# In-memory order storage
orders = {}


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


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