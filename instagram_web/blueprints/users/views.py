from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_name = request.form.get("user_name")
    # breakpoint()
    email = request.form.get("email")
    password = request.form.get("password")
    hashed_password = generate_password_hash(password)

    # if not User.validate_password(password):
    #     flash(f"The password you've inserted is invalid!")
    #     return render_template("users/new.html")

    new_user = User(
        username=user_name,
        email=email,
        password=hashed_password
    )

    if new_user.save():
        flash(f"Welcome {new_user.username}!")
        return redirect(url_for("home"))
    else:
        for error in new_user.errors:
            flash(error)
        return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
