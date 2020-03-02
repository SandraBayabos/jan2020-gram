from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models.user import User
from models.image import Image
from instagram_web.util.s3_uploader import upload_file_to_s3, allowed_file, secure_filename


images_blueprint = Blueprint("images", __name__, template_folder="templates")


@images_blueprint.route("/", methods=["GET"])
def new():
    return render_template("images/new.html")
