from flask import Blueprint, jsonify, request, make_response
from flask_jwt import JWT, jwt_required
from models.user import User
import json

sessions_api_blueprint = Blueprint(
    "sessions_api", __name__, template_folder="templates")


@sessions_api_blueprint.route("/login", methods=["POST"])
def login():
    post_data = request.get_json()

    user = User.get_or_none(email=post_data["email"])

    responseObject = {
        "status": "Success!",
        "message": "User exists!",
        "email": user.email,
        "username": user.username,
        "id": user.id
    }

    return make_response(jsonify(responseObject)), 200
