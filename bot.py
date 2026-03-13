import requests
from flask import Flask, request
import os

app = Flask(__name__)

USERNAME = "chandrda.bathini@gmail.com"
PASSWORD = "Tasty@2461SML"
ACCOUNT = "5WZ78228"

BASE_URL = "https://api.tastytrade.com"

login_payload = {
    "login": USERNAME,
    "password": PASSWORD
}

login = requests.post(BASE_URL + "/sessions", json=login_payload)

print("LOGIN RESPONSE:", login.text)

if login.status_code != 201:
    raise Exception("Tastytrade login failed")

session_token = login.json()["data"]["session-token"]

headers = {
    "Authorization": session_token,
    "Content-Type": "application/json"
}

# ===== TRADE SETTINGS =====
SYMBOL = "TSLA"
QUANTITY = 1


# ===== PLACE ORDER FUNCTION =====
def place_order(side):

    order = {
        "time-in-force": "Day",
        "order-type": "Market",
        "legs": [
            {
                "instrument-type": "Equity",
                "symbol": SYMBOL,
                "quantity": QUANTITY,
                "action": side
            }
        ]
    }

    r = requests.post(
        f"{BASE_URL}/accounts/{ACCOUNT}/orders",
        json=order,
        headers=headers
    )

    print(r.json())


# ===== WEBHOOK =====
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.data.decode("utf-8")

    print("Signal:", data)

    if "LONG" in data:
        place_order("Buy to Open")

    if "SHORT" in data:
        place_order("Sell to Open")

    return jsonify({"status": "order received"})


# ===== START SERVER =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)