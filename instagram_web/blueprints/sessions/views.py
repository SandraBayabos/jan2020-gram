from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from models.user import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")


@sessions_blueprint.route("/", methods=["GET"])
def show():
    return render_template("sessions/new.html")


@sessions_blueprint.route("/new", methods=["POST"])
def sign_in():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_or_none(User.email == email)

    if not user:
        flash("Hmm. We can't seem to find you. Did you insert the correct email?")
        return render_template("sessions/new.html")

    hashed_password = user.password

    if not check_password_hash(hashed_password, password):
        flash("That password is incorrect. Please try again.")
        return render_template("sessions/new.html")

    login_user(user)
    flash(f"Welcome back {user.username}! You are now logged in")
    return redirect(url_for("home"))
