from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import json


from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI server!"}

# Allow frontend requests from any origin (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:5500"] for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Langflow API details
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "25095e61-7c5b-4451-bf69-42eeb621d61b"
FLOW_ID = "2f8bad3b-6076-4ef4-8e8c-d7c0512a89a7"
APPLICATION_TOKEN = "AstraCS:cCUJGDZtioGhIBvzixclTCxq:1b07bfbfbfe8befc18a023038c9a0fe242916157b472a1a646a413278030cb66"

TWEAKS = {
    "GroqModel-wzTk2": {"model_name": "llama-3.2-90b-vision-preview"},
}

def query_langflow(message: str) -> str:
    """Send user message to Langflow API and return AI response"""
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}"
    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    payload = {"input_value": message, "output_type": "chat", "input_type": "chat", "tweaks": TWEAKS}

    response = requests.post(api_url, json=payload, headers=headers)
    try:
        data = response.json()
        return data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    except (KeyError, IndexError, json.JSONDecodeError):
        return "Sorry, I couldn't process that."

@app.post("/chat")
async def chat(request: Request):
    """Handle chat messages from the frontend"""
    data = await request.json()
    user_message = data.get("message", "")
    bot_reply = query_langflow(user_message)
    return {"reply": bot_reply}
