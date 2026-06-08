from flask import Blueprint, jsonify, request
from config import supabase

payments_bp = Blueprint("payments", __name__)

@payments_bp.route("/", methods=["GET"])
def get_all():
    result = supabase.table("payments").select("*, orders(total_amount, order_status, customers(customer_name))").order("payment_date", desc=True).execute()
    return jsonify(result.data)

@payments_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    for field in ["order_id", "amount_paid", "payment_method"]:
        if data.get(field) is None:
            return jsonify({"error": f"{field} is required"}), 400
    data["payment_status"] = "completed"
    result = supabase.table("payments").insert(data).execute()
    supabase.table("orders").update({"order_status": "paid"}).eq("order_id", data["order_id"]).execute()
    return jsonify(result.data[0]), 201