import stripe
import os

from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=1099,
            currency='eur',
            automatic_payment_methods={'enabled': True},
        )

        return jsonify(payment_intent), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/payment-sheet', methods=['POST'])
def payment_sheet():
  # Use an existing Customer ID if this is a returning customer
  customer = stripe.Customer.create()
  ephemeralKey = stripe.EphemeralKey.create(
    customer=customer['id'],
    stripe_version='2023-10-16',
  )
  paymentIntent = stripe.PaymentIntent.create(
    amount=1099,
    currency='eur',
    customer=customer['id'],
    # In the latest version of the API, specifying the `automatic_payment_methods` parameter
    # is optional because Stripe enables its functionality by default.
    automatic_payment_methods={
      'enabled': True,
    },
  )
  return jsonify(paymentIntent=paymentIntent.client_secret,
                 ephemeralKey=ephemeralKey.secret,
                 customer=customer.id,
                 publishableKey='pk_test_51Oq22ZP44uLDl7eGtNaHbbthCuhiZtnG3Y7F13wHrKYclXYVEmnfpZIWGMVeXwUqR2DEoDec6xpQcKQYvzeOHUgu00o91Y8ZVK'

)

if __name__ == '__main__':
    app.run(debug=True)
