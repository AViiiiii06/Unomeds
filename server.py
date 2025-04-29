from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file variables

app = Flask(__name__)
CORS(app)

# Langflow API details
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "25095e61-7c5b-4451-bf69-42eeb621d61b"
FLOW_ID = "2f8bad3b-6076-4ef4-8e8c-d7c0512a89a7"
APPLICATION_TOKEN = os.getenv("LANGFLOW_API_TOKEN")

TWEAKS = {
    "GroqModel-wzTk2": {"model_name": "llama-3.2-90b-vision-preview"},
}

def query_langflow(message: str) -> str:
    """Send user message to Langflow API and return AI response"""
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}"
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": TWEAKS
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    except Exception as e:
        print(f"[ERROR] Langflow query failed: {e}")
        print("Response:", response.text)
        return "Sorry, something went wrong with the AI server."

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask server is running!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"reply": "No message received."}), 400

    bot_reply = query_langflow(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
