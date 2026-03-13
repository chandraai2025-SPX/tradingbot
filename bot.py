from flask import Flask, request
import requests

app = Flask(__name__)

# ---------------------------
# TASTYTRADE LOGIN
# ---------------------------
USERNAME = "chandra.bathini@gmail.com"
PASSWORD = "Tasty@2461SML"
ACCOUNT = "5WZ78228"

BASE_URL = "https://api.tastyworks.com"

# login
login_payload = {
    "login": USERNAME,
    "password": PASSWORD
}

login = requests.post(BASE_URL + "/sessions", json=login_payload)
session_token = login.json()['data']['session-token']

headers = {
    "Authorization": session_token,
    "Content-Type": "application/json"
}

last_signal = None


def buy_tsla():

    order = {
        "time-in-force": "Day",
        "order-type": "Market",
        "legs": [{
            "instrument-type": "Equity",
            "symbol": "TSLA",
            "quantity": 1,
            "action": "Buy to Open"
        }]
    }

    r = requests.post(
        f"{BASE_URL}/accounts/{ACCOUNT}/orders",
        headers=headers,
        json=order
    )

    print("BUY order response:", r.json())


def sell_tsla():

    order = {
        "time-in-force": "Day",
        "order-type": "Market",
        "legs": [{
            "instrument-type": "Equity",
            "symbol": "TSLA",
            "quantity": 1,
            "action": "Sell to Close"
        }]
    }

    r = requests.post(
        f"{BASE_URL}/accounts/{ACCOUNT}/orders",
        headers=headers,
        json=order
    )

    print("SELL order response:", r.json())


@app.route('/webhook', methods=['POST'])
def webhook():

    global last_signal

    data = request.data.decode("utf-8")

    print("Signal received:", data)

    if "long entry" in data.lower() and last_signal != "long":

        last_signal = "long"
        buy_tsla()

    elif "short entry" in data.lower() and last_signal != "short":

        last_signal = "short"
        sell_tsla()

    return "ok", 200


if __name__ == "__main__":
    app.run(port=5000)