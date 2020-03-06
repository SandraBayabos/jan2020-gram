from flask import flash, redirect, request
import braintree
from config import Config

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox,
        merchant_id=Config.BT_MERCHANT_KEY,
        public_key=Config.BT_PUBLIC_KEY,
        private_key=Config.BT_PRIVATE_KEY)
)


def generate_client_token():
    return gateway.client_token.generate()


def complete_transaction(nonce, amount):
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if not result.is_success:
        flash("Donation was unsuccessful!")
        return redirect(request.referrer)

    else:
        return True
    return False
