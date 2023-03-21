import os

from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, JWTManager
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
jwt = JWTManager(app)

hashed_pw = generate_password_hash("1234")
users = [
    {"name": "John", "email": "john@mailinator.com", "password": hashed_pw},
    {"name": "Jane", "email": "jane@mailinator.com", "password": hashed_pw},
]


app.config["SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


def find_by_email(email):
    result = list(filter(lambda user: user["email"] == email, users))
    if len(result) > 0:
        return result[0]
    return None


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", message="Hello World")


@app.route("/login", methods=["POST"])
def login():
    print(request.method)
    email = request.form["email"]
    password = request.form["password"]

    print(email, password)

    if not email or not password:
        return jsonify({"error": "username and password are required"}), 400

    user = find_by_email(email)

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "invalid username or password"}), 401

    access_token = create_access_token(identity=user["email"])

    # return jsonify({"access_token": access_token}), 200
    return render_template("index.html", access_token=access_token), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
