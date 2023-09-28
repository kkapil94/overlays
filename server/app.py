from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
import json


# Connect to MongoDB (Make sure MongoDB is running locally or specify the connection URL)
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/overlays"
db = PyMongo(app).db["overlays"]

def parse_json(data):
    return json.loads(json_util.dumps(data))

# GET Route
@app.route("/",methods=["GET"])
def get_overlays():
    overlays = db.find()
    return jsonify({"success":True,"result":parse_json(overlays)}),201

# POST Route
@app.route("/overlays", methods=["POST"])
def create_overlay():
    data = request.get_json()
    position = data.get("position")
    size = data.get("size")
    content = data.get("content")
    overlay = db.insert_one({"position":position,"size":size,"content":content})
    result = db.find_one({"_id":overlay.inserted_id})
    return jsonify({"message": "Overlay setting created successfully","result":parse_json(result)}), 201

#get_one route
@app.route("/overlays/<overlay_id>", methods=["GET"])
def get_overlay(overlay_id):
    overlay = db.find_one({"_id": ObjectId(overlay_id)})
    if overlay:
        return jsonify({"result":parse_json(overlay)}), 200
    else:
        return jsonify({"success":False,"message": "Overlay not found"}), 404

#update_route
@app.route("/overlays/<overlay_id>", methods=["PUT"])
def update_overlay(overlay_id):
    data = request.get_json()
    position = data.get("position")
    size = data.get("size")
    content = data.get("content")
    result = db.update_one({"_id": ObjectId(overlay_id)}, {"$set": {"position":position,"size":size,"content":content}})
    updated_result = db.find_one({"_id":ObjectId(overlay_id)})
    if result.modified_count>0:
        return jsonify({"success":True,"message": "Overlay updated successfully","result":parse_json(updated_result)}), 200
    else:
        return jsonify({"message": "Overlay not found"}), 404

#delte_route
@app.route("/overlays/<overlay_id>", methods=["DELETE"])
def delete_overlay_setting(overlay_id):
    deleted_result = db.find_one({"_id":ObjectId(overlay_id)})
    result = db.delete_one({"_id": ObjectId(overlay_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Overlay deleted successfully","result":parse_json(deleted_result),"success":True}), 200
    else:
        return jsonify({"message": "Overlay not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
