import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

USERNAME = os.getenv("chandra.bathini@gmail.com")
PASSWORD = os.getenv("Tasty@2461SML")
ACCOUNT = os.getenv("5WZ78228")

BASE_URL = "https://api.tastytrade.com"

session_token = None


def login():
    global session_token

    payload = {
        "login": USERNAME,
        "password": PASSWORD
    }

    r = requests.post(BASE_URL + "/sessions", json=payload)

    try:
        session_token = r.json()["data"]["session-token"]
        print("Login successful")
    except:
        print("Login failed:", r.text)
        session_token = None


def get_position():

    if session_token is None:
        login()

    headers = {"Authorization": session_token}

    r = requests.get(
        BASE_URL + f"/accounts/{ACCOUNT}/positions",
        headers=headers
    )

    try:
        positions = r.json()["data"]["items"]

        for p in positions:
            if p["symbol"] == "TSLA":
                return float(p["quantity"])

    except:
        print("Position fetch error:", r.text)

    return 0


def send_order(action):

    if session_token is None:
        login()

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


@app.route("/")
def home():
    return "Trading bot is running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    signal = data.get("signal")

    position = get_position()

    print("Current TSLA position:", position)

    if signal == "long":

        if position > 0:
            return jsonify({"status": "already long"})

        if position < 0:
            send_order("Buy to Close")

        send_order("Buy to Open")

    elif signal == "short":

        if position < 0:
            return jsonify({"status": "already short"})

        if position > 0:
            send_order("Sell to Close")

        send_order("Sell to Open")

    return jsonify({"status": "order processed"})


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    login()

    app.run(host="0.0.0.0", port=port)