from flask import Flask, request, jsonify
import logging
import os
from logging.handlers import RotatingFileHandler
import signal
import sys

# Load configurations from environment variables
HOST = os.getenv("FLASK_HOST", "0.0.0.0")
PORT = int(os.getenv("FLASK_PORT", 5000))
DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
LOG_LEVEL = os.getenv("FLASK_LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("FLASK_LOG_FILE", "logs/app.log")

# Flask App Initialization
app = Flask(__name__)

# Logging Configuration
log_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log_handler.setLevel(getattr(logging, LOG_LEVEL))

app.logger.addHandler(log_handler)
app.logger.setLevel(getattr(logging, LOG_LEVEL))

@app.route("/", methods=["GET"])
def home():
    app.logger.info("GET request received")
    return jsonify({"message": "Welcome to the Flask Logging API"}), 200

@app.route("/log", methods=["POST"])
def log_message():
    data = request.get_json()
    if not data or "message" not in data:
        app.logger.warning("POST request with missing 'message' field")
        return jsonify({"error": "Missing 'message' field"}), 400
    
    app.logger.info(f"Logged Message: {data['message']}")
    return jsonify({"status": "Message logged"}), 201

@app.route("/logs", methods=["GET"])
def get_logs():
    try:
        with open(LOG_FILE, "r") as log_file:
            logs = log_file.readlines()
        return jsonify({"logs": logs}), 200
    except Exception as e:
        app.logger.error(f"Error reading logs: {e}")
        return jsonify({"error": str(e)}), 500

# Graceful Shutdown Handler
def shutdown_handler(signal_received, frame):
    app.logger.info("Shutting down Flask application...")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
