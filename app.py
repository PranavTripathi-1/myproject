from flask import Flask
from flask import jsonify, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

from routes.item_routes import item_bp

# Load .env variables
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"


mongo = PyMongo(app)

# Make mongo accessible in routes
app.mongo = mongo

# Register routes
app.register_blueprint(item_bp, url_prefix="/items")

@app.route("/")
def home():
    return jsonify({"message": "API is working!"})

if __name__ == "__main__":
    app.run(debug=True)
