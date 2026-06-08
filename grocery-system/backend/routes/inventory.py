from flask import Blueprint, jsonify, request
from config import supabase

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/", methods=["GET"])
def get_all():
    result = supabase.table("inventory")\
        .select("*, products(product_name, price_per_unit, uom(uom_name), suppliers(name))")\
        .execute()
    return jsonify(result.data)

@inventory_bp.route("/low-stock", methods=["GET"])
def low_stock():
    result = supabase.table("inventory")\
        .select("*, products(product_name, uom(uom_name), suppliers(name))")\
        .execute()
    low = [item for item in result.data
           if item["quantity_available"] <= item["minimum_stock_level"]]
    return jsonify(low)

@inventory_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    data = request.get_json()
    result = supabase.table("inventory")\
        .update(data).eq("inventory_id", id).execute()
    return jsonify(result.data[0])