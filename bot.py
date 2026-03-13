from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ==========================
# TASTYTRADE LOGIN
# ==========================

USERNAME = os.getenv("chandra.bathini@gmail.com")
PASSWORD = os.getenv("Tasty@2461SML")

session = requests.Session()

def login_tastytrade():
    url = "https://api.tastyworks.com/sessions"

    payload = {
        "login": USERNAME,
        "password": PASSWORD
    }

    r = session.post(url, json=payload)
    data = r.json()

    if "data" not in data:
        print("Login failed:", data)
        return None

    token = data["data"]["session-token"]
    session.headers.update({"Authorization": token})

    print("Tastytrade login successful")
    return token


# ==========================
# TRADE FUNCTIONS
# ==========================

def buy_tsla():
    print("Executing BUY TSLA (1 share)")
    # Order code would go here
    # For now we just log the signal


def short_tsla():
    print("Executing SELL + SHORT TSLA (1 share)")
    # Order code would go here


# ==========================
# HEALTH CHECK
# ==========================

@app.route("/")
def home():
    return "TSLA Trading Bot Running"


# ==========================
# WEBHOOK FROM TRADINGVIEW
# ==========================

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    print("Webhook received:", data)

    signal = data.get("signal")

    if signal == "long":
        buy_tsla()

    elif signal == "short":
        short_tsla()

    else:
        print("Unknown signal")

    return jsonify({"status": "ok"})


# ==========================
# START SERVER
# ==========================

if __name__ == "__main__":

    login_tastytrade()

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)