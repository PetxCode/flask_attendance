from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

url = "mongodb://localhost:27017"
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

    data = request.get_json()
    print(data)

    result = collection.insert_one(data)
    collection.update_one(
        {"_id": result.inserted_id},
        {"$currentDate": {"createdAt": True}}
    )

    attendance = list(collection.find())
    for i in attendance:
        i["_id"] = str(i["_id"]) 

    return render_template("index.html", attendance=attendance[::-1])

if __name__ == "__main__":
    app.run(debug=True)