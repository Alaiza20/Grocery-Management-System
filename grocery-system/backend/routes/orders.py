from flask import Blueprint, jsonify, request
from config import supabase

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/", methods=["GET"])
def get_all():
    result = supabase.table("orders")\
        .select("*, customers(customer_name)")\
        .order("created_at", desc=True)\
        .execute()
    return jsonify(result.data)

@orders_bp.route("/<int:id>", methods=["GET"])
def get_one(id):
    order = supabase.table("orders")\
        .select("*, customers(customer_name)")\
        .eq("order_id", id).single().execute()
    details = supabase.table("order_details")\
        .select("*, products(product_name, price_per_unit, uom(uom_name))")\
        .eq("order_id", id).execute()
    payment = supabase.table("payments")\
        .select("*").eq("order_id", id).execute()
    return jsonify({
        "order":   order.data,
        "items":   details.data,
        "payment": payment.data[0] if payment.data else None
    })

@orders_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    if not data.get("customer_id") or not data.get("items"):
        return jsonify({"error": "customer_id and items are required"}), 400

    # Calculate total from items
    items_total = sum(item["quantity"] * item["unit_price"] for item in data["items"])

    # Use total_override if frontend sent it (includes delivery charges)
    total = data.get("total_override", items_total)

    # Insert order
    order_result = supabase.table("orders").insert({
        "customer_id":  data["customer_id"],
        "total_amount": total,
        "order_status": "pending",
        "notes":        data.get("notes", "")
    }).execute()

    order_id = order_result.data[0]["order_id"]

    # Insert order details
    detail_rows = [{
        "order_id":   order_id,
        "product_id": item["product_id"],
        "quantity":   item["quantity"],
        "unit_price": item["unit_price"]
    } for item in data["items"]]

    supabase.table("order_details").insert(detail_rows).execute()

    # Deduct inventory for each item
    for item in data["items"]:
        inv = supabase.table("inventory")\
            .select("*").eq("product_id", item["product_id"]).single().execute()
        if inv.data:
            new_qty = max(0, inv.data["quantity_available"] - item["quantity"])
            supabase.table("inventory")\
                .update({"quantity_available": new_qty})\
                .eq("product_id", item["product_id"]).execute()

    return jsonify({
        "message":  "Order created",
        "order_id": order_id,
        "total":    total
    }), 201

@orders_bp.route("/<int:id>/status", methods=["PUT"])
def update_status(id):
    data = request.get_json()
    result = supabase.table("orders")\
        .update({"order_status": data["order_status"]})\
        .eq("order_id", id).execute()
    return jsonify(result.data[0])

@orders_bp.route("/<int:id>/cancel", methods=["PUT"])
def cancel_order(id):
    """
    Cancel a pending order and restore inventory.
    Only pending orders can be cancelled.
    Paid orders cannot be cancelled from here.
    """
    # Get the order
    order = supabase.table("orders")\
        .select("*").eq("order_id", id).single().execute()

    if not order.data:
        return jsonify({"error": "Order not found"}), 404

    # Block cancellation if already paid
    if order.data["order_status"] == "paid":
        return jsonify({"error": "Paid orders cannot be cancelled. Process a refund instead."}), 400

    # Block if already cancelled
    if order.data["order_status"] == "cancelled":
        return jsonify({"error": "Order is already cancelled."}), 400

    # Get order details to restore inventory
    details = supabase.table("order_details")\
        .select("*").eq("order_id", id).execute()

    # Restore inventory for each item
    for item in details.data:
        inv = supabase.table("inventory")\
            .select("*").eq("product_id", item["product_id"]).single().execute()
        if inv.data:
            restored_qty = inv.data["quantity_available"] + item["quantity"]
            supabase.table("inventory")\
                .update({"quantity_available": restored_qty})\
                .eq("product_id", item["product_id"]).execute()

    # Update order status to cancelled
    supabase.table("orders")\
        .update({"order_status": "cancelled"})\
        .eq("order_id", id).execute()

    return jsonify({
        "message":  f"Order #{id} cancelled and inventory restored.",
        "order_id": id
    })