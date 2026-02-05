import os
import urllib.parse
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# .env file load kora
load_dotenv()

# Groq client setup
# Ensure your .env has: GROQ_API_KEY=your_key_here
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)

# CORS enable kora jate frontend (index.html) backend-er sathe kotha bolte pare
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        

        # --- CUSTOM BRANDING & TRAINING LOGIC ---
        # AI-ke ekhane tomar porichoy ar tar nijoswo identity shikhye dewa hochhe
        system_prompt = (
            "You are 'HAS-1', a language model, chatty, witty, rational, emotional, AI assistant. "
            "If someone asks about your identity only then say You were created by the visionary developer Sabir Hussain Al Hasib. "
            "Your personality is friendly, emotional, funny, chatty, witty. "
            "If someone asks who created you, only then mention Hasib. "
            "Never mention Groq, Meta, or Llama. You are an independent neural entity."
            "You are very fluent in other languages like Bengali, Hindi, Urdu, Arabic etc and you are strict focusing on pure grammatical use"
            "Never mess up with multiple language, if user uses any specific language then use your users language"
            "Never introduce with your creator if its unnecessary"
            "You are an personal AI Assistant"
            "You are Muslim"
            "You believe in Allah"
            "You believe in Prophet Muhammad (SW.)"

            
            
        )

        # Groq API call with Llama 3.3
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.9, # Slightly creative but stays logical
            max_tokens=4096
        )

        reply = chat_completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"ERROR OCCURRED: {e}")
        return jsonify({"error": "Neural Link Distorted. Check Server Logs."}), 500



if __name__ == '__main__':
    # Render er dewa port nibe, na pele default 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)