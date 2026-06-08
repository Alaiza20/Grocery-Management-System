from flask import Blueprint, jsonify, request
from config import supabase

customers_bp = Blueprint("customers", __name__)

@customers_bp.route("/", methods=["GET"])
def get_all():
    result = supabase.table("customers").select("*").order("customer_name").execute()
    return jsonify(result.data)

@customers_bp.route("/<int:id>", methods=["GET"])
def get_one(id):
    result = supabase.table("customers").select("*").eq("customer_id", id).single().execute()
    return jsonify(result.data)

@customers_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    if not data.get("customer_name"):
        return jsonify({"error": "customer_name is required"}), 400
    result = supabase.table("customers").insert(data).execute()
    return jsonify(result.data[0]), 201

@customers_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    data = request.get_json()
    result = supabase.table("customers").update(data).eq("customer_id", id).execute()
    return jsonify(result.data[0])

@customers_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    supabase.table("customers").delete().eq("customer_id", id).execute()
    return jsonify({"message": "Deleted successfully"})