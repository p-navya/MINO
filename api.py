from flask import Flask, request, jsonify
from flask_cors import CORS
from views.chatbot import speak_text  # reuse TTS if needed
from db_config import create_user, authenticate_user, save_chat, get_user_chats
from transformers import pipeline
from datetime import datetime

app = Flask(__name__)
CORS(app)

_chatbot = None
def get_bot():
    global _chatbot
    if _chatbot is None:
        _chatbot = pipeline("text2text-generation", model="facebook/blenderbot-400M-distill", framework="pt")
    return _chatbot

@app.post("/api/auth/signup")
def signup():
    data = request.get_json(force=True)
    username = (data or {}).get("username", "").strip()
    password = (data or {}).get("password", "")
    profile_image = (data or {}).get("profile_image")
    if not username or not password:
        return jsonify({"ok": False, "error": "Missing username or password"}), 400
    ok, res = create_user(username, password, profile_image)
    if not ok:
        return jsonify({"ok": False, "error": res}), 400
    return jsonify({"ok": True, "userId": res})

@app.post("/api/auth/login")
def login():
    data = request.get_json(force=True)
    username = (data or {}).get("username", "").strip()
    password = (data or {}).get("password", "")
    ok, user, user_id = authenticate_user(username, password)
    if not ok:
        return jsonify({"ok": False, "error": "Invalid credentials"}), 401
    return jsonify({"ok": True, "userId": user_id, "user": user})

@app.get("/api/chats")
def list_chats():
    user_id = request.args.get("userId", "")
    chats = get_user_chats(user_id) if user_id else {}
    return jsonify({"ok": True, "chats": chats})

@app.post("/api/chats/save")
def save_chats():
    data = request.get_json(force=True) or {}
    user_id = data.get("userId")
    chat_name = data.get("chatName")
    messages = data.get("messages", [])
    if not user_id or not chat_name:
        return jsonify({"ok": False, "error": "Missing userId or chatName"}), 400
    ok = save_chat(user_id, chat_name, messages)
    return jsonify({"ok": ok})

@app.post("/api/chat/ask")
def ask():
    data = request.get_json(force=True) or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"ok": False, "error": "Missing prompt"}), 400
    bot = get_bot()
    try:
        resp = bot(prompt, max_length=100)[0]['generated_text']
        print(f"Raw bot response: {repr(resp)}")  # Debug output
        # Clean up the response to remove any HTML-like content
        import re
        # Remove all HTML tags
        resp = re.sub(r'<[^>]+>', '', resp)
        # Clean up extra whitespace
        resp = ' '.join(resp.split())
        print(f"Cleaned response: {repr(resp)}")  # Debug output
        # If response is empty or too short, provide a fallback
        if len(resp.strip()) < 3:
            resp = "I understand. How can I help you further?"
    except Exception:
        resp = "I'm having trouble right now. Please try again."
    return jsonify({"ok": True, "answer": resp, "time": datetime.now().strftime("%I:%M %p")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


