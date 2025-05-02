from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


APPLICATION_TOKEN = os.getenv("LANGFLOW_API_TOKEN")

def query_langflow(message: str) -> str:
    
    api_url = f"https://api.langflow.astra.datastax.com/lf/25095e61-7c5b-4451-bf69-42eeb621d61b/api/v1/run/bb10bd7c-c478-41f9-b97d-c3f6eeeb9c8b"  

    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    except Exception as e:
        print("[ERROR]", e)
        return "Sorry, there was a problem talking to the AI."

@app.route("/")
def home():
    return jsonify({"message": "UNOMEDS AI Chatbot is running."})

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "Please enter a message."}), 400

    reply = query_langflow(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(port=8000, debug=True)


# updated on May2--SB

