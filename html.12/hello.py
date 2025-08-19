from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS
from dotenv import load_dotenv

# .env fayldan API key o'qish
load_dotenv()

app = Flask(__name__)
CORS(app)  # Frontenddan so'rov yuborish uchun

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    try:
        # OpenAI API chaqirish
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": 500
            }
        )
        result = response.json()
        reply = result.get("choices", [{}])[0].get("message", {}).get("content", "Javob yo'q")
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
