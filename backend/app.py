from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://markmorano.github.io"], supports_credentials=True, methods=["GET", "POST", "OPTIONS"])

API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    contents = data.get("contents", [])

    if not contents:
        return jsonify({"error": "No contents provided"}), 400

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
    payload = {"contents": contents}

    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
        response.raise_for_status()  # Raise error for non-200 status
        result = response.json()

        # Log the raw API response
        print("Gemini API response:", result)

        # Safely extract text
        if "candidates" in result and len(result["candidates"]) > 0:
            text = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            text = "No response from API."

        return jsonify({"text": text})

    except Exception as e:
        print("Error calling Gemini API:", e)
        return jsonify({"error": "Failed to generate response"}), 500



if __name__ == "__main__":
    app.run(debug=True)
