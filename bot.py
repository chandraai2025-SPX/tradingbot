import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

USERNAME = os.getenv("chandra.bathini@gmail.com")
PASSWORD = os.getenv("Tasty@2461SML")
ACCOUNT = os.getenv("5WZ78228")

BASE_URL = "https://api.tastytrade.com"

session_token = None


# ======================
# LOGIN
# ======================

def login():
    global session_token

    payload = {
        "login": USERNAME,
        "password": PASSWORD
    }

    r = requests.post(BASE_URL + "/sessions", json=payload)

    if r.status_code != 201:
        raise Exception("Login failed")

    session_token = r.json()["data"]["session-token"]


login()


# ======================
# GET CURRENT POSITION
# ======================

def get_position():

    headers = {
        "Authorization": session_token
    }

    r = requests.get(
        BASE_URL + f"/accounts/{ACCOUNT}/positions",
        headers=headers
    )

    positions = r.json()["data"]["items"]

    for p in positions:
        if p["symbol"] == "TSLA":
            return float(p["quantity"])

    return 0


# ======================
# SEND ORDER
# ======================

def send_order(action):

    headers = {
        "Authorization": session_token,
        "Content-Type": "application/json"
    }

    order = {
        "order-type": "Market",
        "time-in-force": "Day",
        "legs": [
            {
                "instrument-type": "Equity",
                "symbol": "TSLA",
                "action": action,
                "quantity": 1
            }
        ]
    }

    r = requests.post(
        BASE_URL + f"/accounts/{ACCOUNT}/orders",
        json=order,
        headers=headers
    )

    print("ORDER:", action)
    print("RESPONSE:", r.text)


# ======================
# HEALTH CHECK
# ======================

@app.route("/")
def home():
    return "Trading bot is running"


# ======================
# WEBHOOK
# ======================

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    signal = data.get("signal")

    position = get_position()

    print("Current TSLA position:", position)

    if signal == "long":

        if position > 0:
            print("Already long")
            return jsonify({"status": "already_long"})

        if position < 0:
            send_order("Buy to Close")

        send_order("Buy to Open")


    elif signal == "short":

        if position < 0:
            print("Already short")
            return jsonify({"status": "already_short"})

        if position > 0:
            send_order("Sell to Close")

        send_order("Sell to Open")


    return jsonify({"status": "order_processed"})


# ======================
# RUN SERVER
# ======================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )