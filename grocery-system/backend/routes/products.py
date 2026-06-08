from flask import Blueprint, jsonify, request
from config import supabase

products_bp = Blueprint("products", __name__)

@products_bp.route("/", methods=["GET"])
def get_all():
    result = supabase.table("products").select("*, uom(uom_name), suppliers(name)").order("product_name").execute()
    return jsonify(result.data)

@products_bp.route("/<int:id>", methods=["GET"])
def get_one(id):
    result = supabase.table("products").select("*, uom(uom_name), suppliers(name)").eq("product_id", id).single().execute()
    return jsonify(result.data)

@products_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    if not data.get("product_name") or not data.get("uom_id") or not data.get("price_per_unit"):
        return jsonify({"error": "product_name, uom_id and price_per_unit are required"}), 400
    result = supabase.table("products").insert(data).execute()
    product_id = result.data[0]["product_id"]
    supabase.table("inventory").insert({
        "product_id": product_id,
        "quantity_available": 0,
        "minimum_stock_level": 10
    }).execute()
    return jsonify(result.data[0]), 201

@products_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    data = request.get_json()
    result = supabase.table("products").update(data).eq("product_id", id).execute()
    return jsonify(result.data[0])

@products_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    supabase.table("products").delete().eq("product_id", id).execute()
    return jsonify({"message": "Deleted successfully"})