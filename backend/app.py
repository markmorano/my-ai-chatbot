from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://markmorano.github.io"])

API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    contents = data.get("contents")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-flash-latest:generateContent?key={API_KEY}"
    )

    payload = {
        "contents": contents
    }

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    result = response.json()
    text = result["candidates"][0]["content"]["parts"][0]["text"]

    return jsonify({"text": text})


if __name__ == "__main__":
    app.run(debug=True)
