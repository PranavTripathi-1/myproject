from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId

item_bp = Blueprint("items", __name__)

@item_bp.route("/", methods=["POST"])
def create_item():
    data = request.get_json()
    name = data.get("name")
    desc = data.get("description")

    if not name or not desc:
        return jsonify({"error": "Missing fields"}), 400

    item = {
        "name": name,
        "description": desc
    }

    result = item_bp.mongo.db.items.insert_one(item)
    return jsonify({"id": str(result.inserted_id)}), 201

@item_bp.route("/", methods=["GET"])
def get_all_items():
    items = item_bp.mongo.db.items.find()
    result = []
    for item in items:
        result.append({
            "_id": str(item["_id"]),
            "name": item["name"],
            "description": item["description"]
        })
    return jsonify(result)

@item_bp.route("/<id>", methods=["GET"])
def get_item(id):
    item = item_bp.mongo.db.items.find_one({"_id": ObjectId(id)})
    if not item:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({
        "_id": str(item["_id"]),
        "name": item["name"],
        "description": item["description"]
    })

@item_bp.route("/<id>", methods=["PUT"])
def update_item(id):
    data = request.get_json()
    update_data = {k: v for k, v in data.items() if k in ["name", "description"]}
    result = item_bp.mongo.db.items.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    if result.matched_count == 0:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"message": "Item updated"})

@item_bp.route("/<id>", methods=["DELETE"])
def delete_item(id):
    result = item_bp.mongo.db.items.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"message": "Item deleted"})
