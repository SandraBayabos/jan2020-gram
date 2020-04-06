from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from models.user import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from instagram_web.util.google_oauth import oauth
from instagram_web.util.mailgun import send_message

sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")


@sessions_blueprint.route("/", methods=["GET"])
def new():
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
    send_message("hello", "test", current_user.username)
    flash(f"Welcome back {user.username}! You are now logged in")
    return redirect(url_for("home"))


@sessions_blueprint.route("/logout")
def logout():
    logout_user()
    flash("Successfully logged out. Goodbye!")
    return redirect(url_for("home"))


@sessions_blueprint.route("/google_login", methods=["GET"])
def google_login():
    redirect_uri = url_for('sessions.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route("/google_authorize", methods=["GET"])
def google_authorize():

    token = oauth.google.authorize_access_token()

    if token:
        email = oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
        user = User.get_or_none(User.email == email)

        if not user:
            flash('No user registered with this account.')
            return redirect(url_for('sessions.new'))

    login_user(user)
    flash(f'Welcome back {user.username}')
    return redirect(url_for('users.edit', id=user.id))
