from flask import Flask, request, render_template, jsonify, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json
import os

app = Flask(__name__)

# ── MongoDB Atlas connection ──────────────────────────────────────────────────
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
)
client = MongoClient(MONGO_URI)
db = client["flask_db"]
collection = db["users"]


# ── Route 1: /api  –  read data.json and return as JSON list ─────────────────
@app.route("/api")
def api():
    with open("data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)


# ── Route 2: /  –  show the form ─────────────────────────────────────────────
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", error=None)


# ── Route 3: /submit  –  insert into MongoDB Atlas ───────────────────────────
@app.route("/submit", methods=["POST"])
def submit():
    name  = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    city  = request.form.get("city", "").strip()

    if not name or not email or not city:
        return render_template("index.html", error="All fields are required.")

    try:
        collection.insert_one({"name": name, "email": email, "city": city})
        return redirect(url_for("success"))
    except PyMongoError as e:
        return render_template("index.html", error=str(e))


# ── Route 4: /success  –  confirmation page ──────────────────────────────────
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
