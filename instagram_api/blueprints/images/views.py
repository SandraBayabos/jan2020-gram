from flask import Flask, Blueprint, request, jsonify, make_response
from models.user import User
from models.image import Image
from instagram_web.util.s3_uploader import upload_file_to_s3, allowed_file, secure_filename
from config import Config

images_api_blueprint = Blueprint(
    "images_api", __name__, template_folder="templates")


@images_api_blueprint.route("/upload", methods=["POST"])
def create():
    auth_header = request.headers.get("Authorization")

    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        responseObject = {
            'status': 'failed',
            'message': 'No authorization header found'
        }

        return make_response(jsonify(responseObject)), 401

    user_id = User.decode_auth_token(auth_token)
    user = User.get_or_none(id=user_id)

    file = request.files["image"]

    if user:
        if file and allowed_file(file.filename):
            output = upload_file_to_s3(file, Config.S3_BUCKET)

            upload_image = Image(image=file.filename, user=user.id)

            upload_image.save()
            responseObject = {
                "success": "ok!",
                "message": "Your photo successfully upploaded!"
            }

            return make_response(jsonify(responseObject)), 201

        else:
            responseObject = {
                "status": "failed",
                "message": "Authentication failed!"
            }

            return make_response(jsonify(responseObject)), 401
