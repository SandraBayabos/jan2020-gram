from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, login_required, current_user
from models.user import User
from models.image import Image
from config import Config
from instagram_web.util.s3_uploader import upload_file_to_s3, allowed_file, secure_filename


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_name = request.form.get("user_name")
    email = request.form.get("email")
    password = request.form.get("password")
    # hashed_password = generate_password_hash(password)

    # if not User.validate_password(password):
    #     flash(f"The password you've inserted is invalid!")
    #     return render_template("users/new.html")

    new_user = User(
        username=user_name,
        email=email,
        password=password
    )

    if new_user.save():
        flash(f"Welcome {new_user.username}!")
        login_user(new_user)
        return redirect(url_for("home"))
    else:
        for error in new_user.errors:
            flash(error)
        return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    user = User.get_or_none(User.username == username)

    if current_user:
        if not user:
            flash(
                "We can't seem to find a user with that username. Maybe check your spelling.")
            return redirect(url_for("home"))
        else:
            return render_template("users/show.html", user=user)
    else:
        return abort(401)


@users_blueprint.route('/', methods=["GET"])
def index():
    images = Image.select()
    pass


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_or_none(User.id == id)

    if not str(current_user.id) == id:
        flash("You are not authorized to perform this action. Please sign in first.")
        return redirect(url_for("sessions.new"))

    else:
        if not user:
            flash("We can't seem to find that user. Try again?")
            return redirect(url_for("users.edit"))

        return render_template("users/edit.html", user=user)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_or_none(User.id == id)

    if not str(current_user.id) == id:
        flash("You are not authorized to perform this action. Please sign in first.")
        return redirect(url_for("sessions.new"))

    if not user:
        flash("We can't seem to find that user. Try again?")
        return redirect(url_for("users.edit"))

    new_user_name = request.form.get("new_user_name")
    new_email = request.form.get("new_email")
    # new_password = request.form.get("new_password")

    user.username = new_user_name
    user.email = new_email
    # user.password = new_password

    if user.save():
        flash("Well done! You have just updated your details!")
        return render_template("users/edit.html", user=user)
    else:
        for error in updated_user.errors:
            flash(error)
        return redirect(url_for("users.edit", id=id))


@users_blueprint.route("/upload", methods=["POST"])
def upload_profile():

    user = current_user

    if "user_profile_picture" not in request.files:
        flash('No user_file key in request.files')
        return redirect('/')

    file = request.files["user_profile_picture"]

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, Config.S3_BUCKET)

        user.user_profile_image = file.filename

        update_user_image = User.update(
            user_profile_image=file.filename
        ).where(User.id == current_user.id)

        if update_user_image.execute():
            flash("Success!")
            return redirect(url_for("users.edit", id=current_user.id))
        else:
            for error in user.errors:
                flash(error)
                return redirect(url_for("users.edit", id=current_user.id))
    else:
        flash("That's not an allowed extension. Please upload only JPGs, JPEGs, GIFs, PNGs and PDFs.")
        return redirect(url_for("users.edit", id=current_user.id))
