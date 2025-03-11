from flask import Flask, jsonify, request
from database.config import db
from bson import ObjectId

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "DisasterPredict api is running!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
