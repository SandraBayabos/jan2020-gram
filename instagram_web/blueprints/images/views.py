from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models.user import User
from models.image import Image
from instagram_web.util.s3_uploader import upload_file_to_s3, allowed_file, secure_filename
from config import Config


images_blueprint = Blueprint("images", __name__, template_folder="templates")


@images_blueprint.route("/", methods=["GET"])
@login_required
def new():
    return render_template("images/new.html")


@images_blueprint.route("/new", methods=["POST"])
def create():

    if "image" not in request.files:
        flash("You haven't selected an image. Please choose one and try again.")
        return redirect(url_for('images.new'))

    file = request.files["image"]

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, Config.S3_BUCKET)

        upload_image = Image(image=file.filename, user_id=current_user.id)

        if upload_image.save():
            flash("Successfully uploaded your image!")
            return redirect(url_for("users.show", username=current_user.username))
        else:
            flash('An error occurred. Try again')
            return render_template('images/new.html')
    else:
        for error in upload_image.errors:
            flash(error)
            return redirect(url_for("images.new"))
