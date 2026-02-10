import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)
CORS(app)

# ------------------------------
# SIMPLE IN-MEMORY SESSION STORE
# ------------------------------
# NOTE: This resets when server restarts (OK for v1)
sessions = {}
MAX_HISTORY = 10  # last 10 messages only (cost control)

# ------------------------------
# SYSTEM PROMPT (CLEANED)
# ------------------------------
SYSTEM_PROMPT = (
    "You are HAS-1, a friendly, witty, rational, and emotional AI assistant. "
    "Only mention your creator (Sabir Hussain Al Hasib) if explicitly asked. "
    "You are multilingual and must reply strictly in the user's language. "
    "Do not mix languages. Be grammatically correct. "
    "You are personal, respectful, and helpful."
)


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json or {}
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        # Create new session if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
            sessions[session_id] = []

        # Initialize session if missing
        if session_id not in sessions:
            sessions[session_id] = []

        # Append user message
        sessions[session_id].append({"role": "user", "content": user_message})

        # Trim history (cost control)
        sessions[session_id] = sessions[session_id][-MAX_HISTORY:]

        # Build message payload
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(sessions[session_id])

        # Groq API call
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.9,
            max_tokens=2048
        )

        reply = completion.choices[0].message.content

        # Append assistant reply
        sessions[session_id].append({"role": "assistant", "content": reply})
        sessions[session_id] = sessions[session_id][-MAX_HISTORY:]

        return jsonify({
            "reply": reply,
            "session_id": session_id
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Server error"}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
