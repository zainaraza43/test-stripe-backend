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

if __name__ == '__main__':
    app.run(debug=True)
