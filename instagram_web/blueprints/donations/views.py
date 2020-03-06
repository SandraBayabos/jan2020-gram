from flask import Blueprint, flash, redirect, url_for, request, render_template
from models.image import Image
from models.donation import Donation
from flask_login import login_required, current_user
from instagram_web.util.braintree import generate_client_token, complete_transaction
from instagram_web.util.mailgun import send_message

donations_blueprint = Blueprint(
    "donations", __name__, template_folder="templates")


@donations_blueprint.route("/<image_id>/new", methods=["GET"])
@login_required
def new(image_id):
    image = Image.get_or_none(Image.id == image_id)

    if not image:
        flash("No image found with that id", "warning")
        return redirect(url_for("users.index"))

    client_token = generate_client_token()

    if not client_token:
        flash("Unable to get client token")
        return redirect(url_for("users.index"))
    else:
        return render_template("donations/new.html", image=image, client_token=client_token)

    return render_template("donations/new.html", image=image)


@donations_blueprint.route("/<image_id>/checkout", methods=["POST"])
def create(image_id):
    payment_nonce = request.form.get("payment_nonce")
    amount = request.form.get("donation_amount")
    image = Image.get_or_none(Image.id == image_id)
    email = image.user.email

    if not image:
        flash("Unable to find image. Please try again.")
        return redirect(url_for("users.index"))

    if not amount or round(int(amount), 2) == 0:
        flash("That is not a proper amount. Please insert a valid amount.")
        return redirect(url_for("donations.new", image_id=image.id))

    if not payment_nonce:
        flash("Error with payment system. Please try again.")
        return redirect(url_for("donations.new", image_id=image.id))

    if not complete_transaction(payment_nonce, amount):
        flash("Something went wrong. Please check your details or the amount and try again")
        return redirect(url_for("donations.new", image_id=image.id))

    # result = gateway.transaction.sale({
    #     "amount": amount,
    #     "payment_method_nonce": nonce,
    #     "options": {
    #         "submit_for_settlement": True
    #     }
    # })

    # if not result.is_success:
    #     flash("Donation was unsuccessful!")
    #     return redirect(request.referrer)

    new_donation = Donation(
        user_id=current_user.id,
        amount=amount,
        image_id=image.id
    )

    if not new_donation.save():
        flash("Unable to complete the transaction. Please try again.")
        return redirect(url_for("donations.new", image_id=image.id))

    send_message(amount, image.image, current_user.username)

    flash("Donation successful!")
    return redirect(url_for("users.show", username=image.user.username))
