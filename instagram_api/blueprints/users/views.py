from flask import Blueprint, jsonify, make_response
from flask_jwt import JWT, jwt_required
from models.user import User
from playhouse.shortcuts import model_to_dict


users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()

    user_data = []

    for user in users:
        user = model_to_dict(user)
        user_data.append(user)

    return jsonify(user_data), 200


@users_api_blueprint.route("/new", methods=["POST"])
def new():
    post_data = request.get_json()

    try:
        new_user = User(
            username=post_data['username'],
            email=post_data['email'].lower(),
            password=post_data['password']
        )
    except:
        responseObject = {
            'status': 'failed',
            'message': ['All fields are required!']
        }

        return make_response(jsonify(responseObject)), 400

    if new_user.save():
        auth_token = new_user.encode_auth_token(new_user.id)

        responseObject = {
            "status": "success!",
            "message": "successfully created a new user and signed in!",
            'auth_token': auth_token.decode(),
            "user": {
                "id": int(new_user.id),
                "username": new_user.username
            }
        }

        return make_response(jsonify(responseObject)), 201


# @users_api_blueprint("/<username>", methods=["POST"])
# @jwt_required
# def show(username):
#     user = User.get_or_none(User.username == username)

#     if not user:
#         resp = {
#             "message": "No user found with that username!",
#             "ok": False
#         }

#         return jsonify(resp)

#     resp = {
#         "message": "Found user with that username",
#         "user": {
#             "id": user.id,
#             "username": user.username,
#             "email": user.email
#         },
#         "ok": True
#     }
#     return jsonify(resp)
