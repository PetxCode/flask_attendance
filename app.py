from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)


def _serialize_attendance(records):
    serialized = []
    for item in records:
        payload = dict(item)
        payload["_id"] = str(payload.get("_id"))
        if payload.get("createdAt") and hasattr(payload["createdAt"], "isoformat"):
            payload["createdAt"] = payload["createdAt"].isoformat()
        serialized.append(payload)
    return serialized

# url = "mongodb://localhost:27017"
url = "mongodb+srv://nextteachnow:nextteachnow@cluster0.ozfyjn7.mongodb.net/churchDB?appName=Cluster0"
client = MongoClient(url)
db = client["churchDB"]
collection = db["attendence"]

@app.route("/")
def index():
    attendance = list(collection.find())
    for i in attendance:
        i["_id"] = str(i["_id"]) 

    return render_template("index.html", attendance=attendance[::-1])

@app.route("/add_member", methods=["POST"])
def add_member():
    data = request.get_json(silent=True) or request.form.to_dict()

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    result = collection.insert_one(data)
    collection.update_one(
        {"_id": result.inserted_id},
        {"$currentDate": {"createdAt": True}}
    )

    attendance = list(collection.find())
    return jsonify({"success": True, "data": _serialize_attendance(attendance[::-1])})

if __name__ == "__main__":
    app.run(debug=True)
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port, debug=True)