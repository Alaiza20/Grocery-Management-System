# Import Blueprint to organize routes
# jsonify converts Python data into JSON
# request gets data sent by the user
from flask import Blueprint, jsonify, request

# Import Supabase database connection

from config import supabase


# Create a blueprint for UOM routes
uom_bp = Blueprint("uom", __name__)


# GET all UOM records
# Example: /api/uom/
@uom_bp.route("/", methods=["GET"])
def get_all():

    # Select all rows from uom table and sort by uom_name
    result = supabase.table("uom").select("*").order("uom_name").execute()

    # Return data as JSON response
    return jsonify(result.data)


# GET single UOM record by ID
# Example: /api/uom/1
@uom_bp.route("/<int:id>", methods=["GET"])
def get_one(id):

    # Find record where uom_id matches the given id
    result = supabase.table("uom").select("*").eq("uom_id", id).single().execute()

    # Return single record
    return jsonify(result.data)


# CREATE a new UOM record
# Example: POST /api/uom/
@uom_bp.route("/", methods=["POST"])
def create():

    # Get JSON data sent from frontend/user
    data = request.get_json()

    # Check if uom_name exists
    if not data.get("uom_name"):

        # Return error if missing
        return jsonify({
            "error": "uom_name is required"
        }), 400

    # Insert new record into uom table
    result = supabase.table("uom").insert(data).execute()

    # Return newly created record with status code 201
    return jsonify(result.data[0]), 201


# UPDATE an existing UOM record
# Example: PUT /api/uom/1
@uom_bp.route("/<int:id>", methods=["PUT"])
def update(id):

    # Get updated data from request
    data = request.get_json()

    # Update record where uom_id matches the given id
    result = supabase.table("uom").update(data).eq("uom_id", id).execute()

    # Return updated record
    return jsonify(result.data[0])


# DELETE a UOM record
# Example: DELETE /api/uom/1
@uom_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):

    # Delete record where uom_id matches the given id
    supabase.table("uom").delete().eq("uom_id", id).execute()

    # Return success message
    return jsonify({
        "message": "Deleted successfully"
    })