# Import Flask framework to create the backend server
# jsonify converts Python dictionaries into JSON responses
from flask import Flask, jsonify

# Import CORS to allow frontend and backend communication
# Example:
# React frontend (localhost:3000) can communicate with Flask backend (localhost:5000)
from flask_cors import CORS

# Import load_dotenv to load environment variables from .env file
from dotenv import load_dotenv

# Import os module to access environment variables
import os


# Load all variables from .env file
load_dotenv()


# Create a Flask app and use this file’s location as the base reference
app = Flask(__name__)


# Set a secret key for sessions and security
# If SECRET_KEY is not found in .env,
# it will use "dev-secret" as default value
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")


# Enable CORS for all routes
# This allows frontend applications to access backend APIs
# CORS allows frontend (different origin like React-port 3000 and flask - port 5000) to access this backend API
CORS(app)


# Import blueprint modules from routes folder
# Each blueprint handles a specific feature/module
from routes.uom import uom_bp
from routes.products import products_bp
from routes.customers import customers_bp
from routes.orders import orders_bp
from routes.payments import payments_bp
from routes.suppliers import suppliers_bp
from routes.inventory import inventory_bp


# Register UOM routes
# Example endpoint:
# /api/uom/
app.register_blueprint(uom_bp, url_prefix="/api/uom")


# Register product routes
# Example endpoint:
# /api/products/
app.register_blueprint(products_bp, url_prefix="/api/products")

app.register_blueprint(customers_bp, url_prefix="/api/customers")


app.register_blueprint(orders_bp, url_prefix="/api/orders")


app.register_blueprint(payments_bp, url_prefix="/api/payments")


app.register_blueprint(suppliers_bp, url_prefix="/api/suppliers")


app.register_blueprint(inventory_bp, url_prefix="/api/inventory")


# Simple testing route
# Used to check whether Flask server is running correctly
@app.route("/api/ping")
def ping():

    # Return JSON response
    return jsonify({
        "status": "ok",
        "message": "Flask is running"
    })


# Database testing route
# Used to verify Supabase database connection
@app.route("/api/test-db")
def test_db():

    try:
        # Import Supabase connection object from config.py
        from config import supabase

        # Fetch one record from uom table
        result = supabase.table("uom").select("*").limit(1).execute()

        # Return success response with sample data
        return jsonify({
            "status": "ok",
            "message": "Supabase connected successfully",
            "sample": result.data
        })

    except Exception as e:

        # Return error response if database connection fails
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Run Flask server only when this file is executed directly
if __name__ == "__main__":

    # Start Flask server in debug mode on port 5000
    # debug=True — server auto-restarts when you save changes
    app.run(debug=True, port=5000, host="0.0.0.0")
