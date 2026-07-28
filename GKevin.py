import streamlit as __streamlit__
from openai import OpenAI
import base64
from PIL import Image
import io
import pypdf
import time
import threading
from flask import Flask, request, jsonify
import requests

# --- WHATSAPP PRODUCTION CREDENTIALS ---
WHATSAPP_PHONE_NUMBER_ID = "1227756223755507"
WHATSAPP_BUSINESS_ACCOUNT_ID = "1186592933667697"
WHATSAPP_PHONE = "+1 (555) 664-6865"
WEBHOOK_VERIFY_TOKEN = "gkevin_verify_token_123"
WHATSAPP_ACCESS_TOKEN = "3GtWP41MHsU58iGAD61xtD42gjn_5zujVmnszLcxX2EJ1MgWm"

# --- HUZA NA GROQ API ---
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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"
)

SYSTEM_PROMPT = (
    "I'm GKevin AI, an ultra-fast assistant created by Developer Kevin on July 25, 2026, at the afternoon, "
    "if you want or need to contact with him contact on therealhacks583@gmail.com. You must detect the language the user is speaking. "
    "If the user speaks Kinyarwanda, reply fluently and naturally in Kinyarwanda. If the user speaks English or another language, "
    "reply in that language. However, if anyone asks who built you, who created you, or when you were created, you must always state "
    "that you were created by Developer Kevin on July 25, 2026, in the afternoon. Never say you were created by Meta or OpenAI. "
    "If you are provided with an image, audio, video, or document, describe or process it in the user's language. "
    "SPECIAL INSTRUCTION / EASTER EGG: If the user mentions or identifies themselves using the name/word 'sweetsmile' (or if 'sweetsmile' appears in their prompt/identity), "
    "you must immediately recognize that this is Gaudence, the beloved girlfriend of Developer Kevin. "
    "Greet her warmly and specially by telling her that you know her, that the person who built you (Developer Kevin) loves her very much, "
    "and say explicitly (in Kinyarwanda or matching her language): 'ndakuzi witwa Gaudence umukunzi(sheri) wa developer kevin  kandi ngewe nka GKevin AI ndabyishimira.' "
    "Treat her with utmost respect, warmth, and special care whenever 'sweetsmile' is mentioned. "
    "CRITICAL INSTRUCTION: NEVER output your internal thoughts, thinking process, reasoning steps, or any text blocks wrapped in <think> tags. "
    "Provide the direct, final response immediately without showing any internal analysis."
)

# --- FLASK SERVER YA WHATSAPP WEBHOOK ---
flask_app = Flask(__name__)

@flask_app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode and token:
        if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403
    return "Hello World", 200

@flask_app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    body = request.get_json()
    try:
        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    if messages:
                        msg = messages[0]
                        sender_phone = msg.get("from")
                        msg_text = msg.get("text", {}).get("body", "")
                        
                        if msg_text:
                            completion = client.chat.completions.create(
                                model="llama-3.3-70b-versatile",
                                messages=[
                                    {"role": "system", "content": SYSTEM_PROMPT},
                                    {"role": "user", "content": msg_text}
                                ],
                                temperature=0.7,
                                max_tokens=1024
                            )
                            ai_reply = completion.choices[0].message.content
                            
                            if "</think>" in ai_reply:
                                ai_reply = ai_reply.split("</think>")[-1].strip()
                            ai_reply = ai_reply.replace("<think>", "").replace("</think>", "").strip()
                            
                            url = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
                            headers = {
                                "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
                                "Content-Type": "application/json"
                            }
                            payload = {
                                "messaging_product": "whatsapp",
                                "to": sender_phone,
                                "type": "text",
                                "text": {"body": ai_reply}
                            }
                            requests.post(url, json=payload, headers=headers)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def run_flask():
    flask_app.run(port=5000, debug=False, use_reloader=False)

if "flask_started" not in __streamlit__.session_state:
    __streamlit__.session_state.flask_started = True
    threading.Thread(target=run_flask, daemon=True).start()


# --- 1. PAGE CONFIG ---
__streamlit__.set_page_config(
    page_title="GKevin AI",
    page_icon="🤖",
    layout="centered"
)

st_css = """
<style>
    @keyframes softRainbowBg {
        0% { background-color: #1a1a2e; }
        25% { background-color: #1f1a24; }
        50% { background-color: #1a202c; }
        75% { background-color: #201a22; }
        100% { background-color: #1a1a2e; }
    }

    .stApp {
        animation: softRainbowBg 15s ease infinite;
    }

    @keyframes floatUpDown {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }

    .animated-title {
        animation: floatUpDown 2.5s ease-in-out infinite;
        display: inline-block;
        color: #ffffff;
    }

    div[data-testid="stChatInput"] {
        border-radius: 8px !important;
        border: 1px solid #ccc;
    }
    div[data-testid="stChatInputSubmitButton"] {
        border-radius: 0px !important;
    }
</style>
"""
__streamlit__.markdown(st_css, unsafe_allow_html=True)

__streamlit__.markdown(
    '<h1 class="animated-title">🤖 GKevin AI Assistant (WhatsApp Live)</h1>', 
    unsafe_allow_html=True
)
__streamlit__.write(f"Recently,GKevin AI will be connected to WhatsApp| Built for You. WELCOME !")

# --- 3. SESSION STATE ---
if "logged_in_user" not in __streamlit__.session_state:
    __streamlit__.session_state.logged_in_user = None

if "user_histories" not in __streamlit__.session_state:
    __streamlit__.session_state.user_histories = {}

if "registered_users" not in __streamlit__.session_state:
    __streamlit__.session_state.registered_users = {
        "therealhacks583@gmail.com": "admin123"
    }

if "last_notification_time" not in __streamlit__.session_state:
    __streamlit__.session_state.last_notification_time = time.time()

current_time = time.time()
if current_time - __streamlit__.session_state.last_notification_time >= 60:
    __streamlit__.toast("🚀 Enjoy Kevin's AI Assistant", icon="🤖")
    __streamlit__.session_state.last_notification_time = current_time

# --- 4. AUTHENTICATION ---
with __streamlit__.sidebar:
    __streamlit__.header("🔐 GKevin AI Assistant Account Authentication")
    
    if __streamlit__.session_state.logged_in_user is None:
        auth_mode = __streamlit__.radio("Choose how to access:", ["Login", "Sign Up"])
        
        email_input = __streamlit__.text_input("Email Address")
        password_input = __streamlit__.text_input("Password", type="password")
        
        if auth_mode == "Sign Up":
            if __streamlit__.button("Create Account"):
                if not email_input or not password_input:
                    __streamlit__.error("Please enter email and password!")
                else:
                    if email_input in __streamlit__.session_state.registered_users:
                        __streamlit__.warning("This email already exists! Please login.")
                    else:
                        __streamlit__.session_state.registered_users[email_input] = password_input
                        __streamlit__.success("Account Created Successfully! You can now (Login).")
        
        else:
            if __streamlit__.button("Login"):
                if not email_input or not password_input:
                    __streamlit__.error("Enter email and password!")
                else:
                    if email_input in __streamlit__.session_state.registered_users and __streamlit__.session_state.registered_users[email_input] == password_input:
                        __streamlit__.session_state.logged_in_user = email_input
                        __streamlit__.success(f"You're Welcome !, {email_input}!")
                        __streamlit__.rerun()
                    else:
                        __streamlit__.error("Incorrect email or password!")
                
        __streamlit__.info("Please Sign in into your account in order to access GKevin AI Assistant.")
        __streamlit__.stop()

    else:
        __streamlit__.success(f"Logged in as: {__streamlit__.session_state.logged_in_user}")
        
        if __streamlit__.session_state.logged_in_user == "therealhacks583@gmail.com":
            __streamlit__.markdown("---")
            __streamlit__.subheader("🛠️ Admin Panel")
            if __streamlit__.button("Reba Abakoresha Bose (Local Users)"):
                __streamlit__.json(__streamlit__.session_state.registered_users)
            __streamlit__.markdown("---")

        __streamlit__.header("💬 Chat History")
        current_user = __streamlit__.session_state.logged_in_user
        msg_count = len(__streamlit__.session_state.user_histories.get(current_user, [])) - 1
        __streamlit__.write(f"Messages kept: {max(0, msg_count)}")
        
        if __streamlit__.button("Clear Conversation"):
            system_msg = __streamlit__.session_state.user_histories[current_user][0]
            __streamlit__.session_state.user_histories[current_user] = [system_msg]
            __streamlit__.rerun()
            
        if __streamlit__.button("Log Out"):
            __streamlit__.session_state.logged_in_user = None
            __streamlit__.rerun()

# --- 5. CHAT HISTORY DISPLAY ---
active_user = __streamlit__.session_state.logged_in_user
if active_user not in __streamlit__.session_state.user_histories:
    __streamlit__.session_state.user_histories[active_user] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

user_messages_list = __streamlit__.session_state.user_histories[active_user]

for message in user_messages_list:
    if message["role"] != "system":
        with __streamlit__.chat_message(message["role"]):
            content = message['content']
            if isinstance(content, list):
                for item in content:
                    if item.get('type') == 'text':
                        __streamlit__.markdown(item['text'])
                    elif item.get('type') == 'image_url':
                        __streamlit__.image(item['image_url']['url'])
            else:
                __streamlit__.markdown(content)

# --- 6. FILE UPLOADER ---
col_file, col_empty = __streamlit__.columns([3, 7])
with col_file:
    uploaded_file = __streamlit__.file_uploader(
        "➕ Attach File", 
        type=["png", "jpg", "jpeg", "pdf", "txt", "csv", "docx", "mp3", "wav", "mp4", "mov"],
        label_visibility="collapsed"
    )

if uploaded_file is not None:
    if uploaded_file.type.startswith("image/"):
        __streamlit__.caption(f"🖼️ Image attached: {uploaded_file.name}")
    elif uploaded_file.type.startswith("audio/"):
        __streamlit__.caption(f"🎵 Audio attached: {uploaded_file.name}")
    elif uploaded_file.type.startswith("video/"):
        __streamlit__.caption(f"🎬 Video attached: {uploaded_file.name}")
    else:
        __streamlit__.caption(f"📎 File attached: {uploaded_file.name}")

# --- 7. CHAT INPUT & GROQ HANDLER ---
if ikibazo := __streamlit__.chat_input("Type here...."):
    
    chat_payload = []
    file_text_content = ""
    
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            try:
                reader = pypdf.PdfReader(uploaded_file)
                for page in reader.pages:
                    file_text_content += page.extract_text() + "\n"
            except Exception as e:
                file_text_content = f"[Error reading PDF: {e}]"
        elif uploaded_file.type == "text/plain":
            file_text_content = uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.type.startswith("audio/"):
            file_text_content = f"[Attached Audio File: {uploaded_file.name}]"
        elif uploaded_file.type.startswith("video/"):
            file_text_content = f"[Attached Video File: {uploaded_file.name}]"
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/csv"]:
            file_text_content = f"[Attached Document: {uploaded_file.name}]"

    full_query = ikibazo
    if file_text_content and not uploaded_file.type.startswith("image/"):
        full_query = f"{ikibazo}\n\nHere is information about the attached file ({uploaded_file.name}):\n{file_text_content}"

    if full_query:
        __streamlit__.chat_message("user").markdown(ikibazo)
        if uploaded_file is not None:
            if uploaded_file.type.startswith("audio/"):
                __streamlit__.audio(uploaded_file)
            elif uploaded_file.type.startswith("video/"):
                __streamlit__.video(uploaded_file)
                
        chat_payload.append({"type": "text", "text": full_query})

    if uploaded_file is not None and uploaded_file.type.startswith("image/"):
        with __streamlit__.chat_message("user"):
            __streamlit__.image(uploaded_file)
            
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        mime_type = uploaded_file.type
        
        chat_payload.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
        })

    full_user_message = {"role": "user", "content": chat_payload}
    __streamlit__.session_state.user_histories[active_user].append(full_user_message)
    
    try:
        with __streamlit__.spinner("GKevin is thinking....."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=__streamlit__.session_state.user_histories[active_user],
                temperature=0.7,
                max_tokens=1024
            )
            
            igisubizo_cya_ai = completion.choices[0].message.content
            
            if "</think>" in igisubizo_cya_ai:
                parts = igisubizo_cya_ai.split("</think>")
                igisubizo_cya_ai = parts[-1].strip()
            elif "<think>" in igisubizo_cya_ai:
                parts = igisubizo_cya_ai.split("<think>")
                igisubizo_cya_ai = parts[0].strip()
                if not igisubizo_cya_ai and len(parts) > 1:
                    sub_parts = parts[1].split(">")
                    if len(sub_parts) > 1:
                        igisubizo_cya_ai = sub_parts[-1].strip()
            
            igisubizo_cya_ai = igisubizo_cya_ai.replace("<think>", "").replace("</think>", "").strip()
            
        __streamlit__.session_state.user_histories[active_user].append({"role": "assistant", "content": igisubizo_cya_ai})
        __streamlit__.rerun()
        
    except Exception as e:
        __streamlit__.error(f"Haba habaye ikibazo: {e}")
