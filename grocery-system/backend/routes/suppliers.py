# Import Blueprint to organize routes
# jsonify converts Python data into JSON format
# request gets data sent from frontend/user
from flask import Blueprint, jsonify, request

# Import Supabase database connection
from config import supabase


# Create a blueprint for supplier routes
suppliers_bp = Blueprint("suppliers", __name__)


# GET all supplier records
# Example: /api/suppliers/
@suppliers_bp.route("/", methods=["GET"])
def get_all():

    # Fetch all suppliers and sort them by name
    result = supabase.table("suppliers").select("*").order("name").execute()

    # Return supplier data as JSON
    return jsonify(result.data)


# GET one supplier by ID
# Example: /api/suppliers/1
@suppliers_bp.route("/<int:id>", methods=["GET"])
def get_one(id):

    # Find supplier where supplier_id matches given id
    result = supabase.table("suppliers").select("*").eq("supplier_id", id).single().execute()

    # Return supplier data
    return jsonify(result.data)


# CREATE a new supplier
# Example: POST /api/suppliers/ 
# post -create data
# get -read data
@suppliers_bp.route("/", methods=["POST"])
def create():

    # Get JSON data from request
    data = request.get_json()

    # Check if supplier name exists
    if not data.get("name"):

        # Return error if name is missing
        return jsonify({
            "error": "name is required"
        }), 400

    # Insert new supplier into suppliers table
    result = supabase.table("suppliers").insert(data).execute()

    # Return created supplier with status code 201
    return jsonify(result.data[0]), 201


# UPDATE supplier by ID
# Example: PUT /api/suppliers/1
@suppliers_bp.route("/<int:id>", methods=["PUT"])
def update(id):

    # Get updated data from request
    data = request.get_json()

    # Update supplier where supplier_id matches given id
    result = supabase.table("suppliers").update(data).eq("supplier_id", id).execute()

    # Return updated supplier data
    return jsonify(result.data[0])


# DELETE supplier by ID
# Example: DELETE /api/suppliers/1
@suppliers_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):

    # Delete supplier where supplier_id matches given id
    supabase.table("suppliers").delete().eq("supplier_id", id).execute()

    # Return success message
    return jsonify({
        "message": "Deleted successfully"
    })