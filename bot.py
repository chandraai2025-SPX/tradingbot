from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

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

    try:
        data = r.json()

        if "data" not in data:
            print("Login failed:", data)
            return None

        token = data["data"]["session-token"]
        session.headers.update({"Authorization": token})

        print("Tastytrade login successful")
        return token

    except Exception as e:
        print("Login error:", e)
        return None


@app.route("/")
def home():
    return "TSLA Trading Bot Running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    print("Webhook received:", data)

    login_tastytrade()

    signal = data.get("signal")

    if signal == "long":
        print("BUY 1 TSLA")

    elif signal == "short":
        print("SELL + SHORT 1 TSLA")

    else:
        print("Unknown signal")

    return jsonify({"status": "ok"})