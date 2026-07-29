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

# --- HUZA NA GROQ API UKORESHEJE STREAMLIT SECRETS ---
try:
    groq_api_key_val = __streamlit__.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key_val = "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"

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key_val
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
__streamlit__.write(f"Recently, GKevin AI will be connected to WhatsApp | Built for You. WELCOME !")

# --- 3. SESSION STATE FOR MULTI-CHAT HISTORY (GEMINI STYLE) ---
if "logged_in_user" not in __streamlit__.session_state:
    __streamlit__.session_state.logged_in_user = None

if "registered_users" not in __streamlit__.session_state:
    __streamlit__.session_state.registered_users = {
        "therealhacks583@gmail.com": "admin123"
    }

# Dictionary yo kubika amateka y'ibiganiro byose by'abakoresha (User Chats Sessions)
if "chats" not in __streamlit__.session_state:
    __streamlit__.session_state.chats = {} # {user_email: {chat_id: {"title": str, "messages": [...]}}}

if "current_chat_id" not in __streamlit__.session_state:
    __streamlit__.session_state.current_chat_id = None

if "last_notification_time" not in __streamlit__.session_state:
    __streamlit__.session_state.last_notification_time = time.time()

current_time = time.time()
if current_time - __streamlit__.session_state.last_notification_time >= 60:
    __streamlit__.toast("🚀 Enjoy Kevin's AI Assistant", icon="🤖")
    __streamlit__.session_state.last_notification_time = current_time


# --- 4. AUTHENTICATION & SIDEBAR CHAT HISTORY ---
with __streamlit__.sidebar:
    __streamlit__.header("🔐 Account Authentication")
    
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
                        
                        # Shaka cyangwa urebe niba afite chat ya mbere
                        user_email = email_input
                        if user_email not in __streamlit__.session_state.chats:
                            __streamlit__.session_state.chats[user_email] = {}
                        
                        if not __streamlit__.session_state.chats[user_email]:
                            init_id = f"chat_{int(time.time())}"
                            __streamlit__.session_state.chats[user_email][init_id] = {
                                "title": "New Chat",
                                "messages": [{"role": "system", "content": SYSTEM_PROMPT}]
                            }
                            __streamlit__.session_state.current_chat_id = init_id
                        else:
                            __streamlit__.session_state.current_chat_id = list(__streamlit__.session_state.chats[user_email].keys())[0]

                        __streamlit__.success(f"You're Welcome !, {email_input}!")
                        __streamlit__.rerun()
                    else:
                        __streamlit__.error("Incorrect email or password!")
                
        __streamlit__.info("Please Sign in into your account in order to access GKevin AI Assistant.")
        __streamlit__.stop()

    else:
        current_user = __streamlit__.session_state.logged_in_user
        __streamlit__.success(f"Logged in: {current_user}")
        
        # Ongeraho uburyo bwo gukora New Chat nka Gemini
        if __streamlit__.button("➕ New Chat", use_container_width=True):
            new_id = f"chat_{int(time.time())}"
            if current_user not in __streamlit__.session_state.chats:
                __streamlit__.session_state.chats[current_user] = {}
            
            __streamlit__.session_state.chats[current_user][new_id] = {
                "title": "New Chat",
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}]
            }
            __streamlit__.session_state.current_chat_id = new_id
            __streamlit__.rerun()

        __streamlit__.markdown("---")
        __streamlit__.markdown("### 💬 Recents (Chat History)")

        # Niba uyu mukoresha afite chats, zerekanemo zose nk'urutonde muri Sidebar
        if current_user in __streamlit__.session_state.chats:
            user_chats = __streamlit__.session_state.chats[current_user]
            for c_id, c_data in list(user_chats.items()):
                title_label = c_data["title"]
                if len(title_label) > 25:
                    title_label = title_label[:22] + "..."
                
                # Iyo ukanze kuri buto y'ikiganiro cyashize irayifungura
                is_selected = (c_id == __streamlit__.session_state.current_chat_id)
                button_type = "primary" if is_selected else "secondary"
                
                col_c1, col_c2 = __streamlit__.columns([4, 1])
                with col_c1:
                    if __streamlit__.button(title_label, key=f"select_{c_id}", use_container_width=True, type=button_type):
                        __streamlit__.session_state.current_chat_id = c_id
                        __streamlit__.rerun()
                with col_c2:
                    if __streamlit__.button("🗑️", key=f"del_{c_id}"):
                        del user_chats[c_id]
                        if user_chats:
                            __streamlit__.session_state.current_chat_id = list(user_chats.keys())[0]
                        else:
                            new_id = f"chat_{int(time.time())}"
                            user_chats[new_id] = {
                                "title": "New Chat",
                                "messages": [{"role": "system", "content": SYSTEM_PROMPT}]
                            }
                            __streamlit__.session_state.current_chat_id = new_id
                        __streamlit__.rerun()

        __streamlit__.markdown("---")
        if current_user == "therealhacks583@gmail.com":
            __streamlit__.subheader("🛠️ Admin Panel")
            if __streamlit__.button("Reba Abakoresha Bose (Local Users)"):
                __streamlit__.json(__streamlit__.session_state.registered_users)
            __streamlit__.markdown("---")
            
        if __streamlit__.button("Log Out"):
            __streamlit__.session_state.logged_in_user = None
            __streamlit__.session_state.current_chat_id = None
            __streamlit__.rerun()


# --- 5. KWEMEZA NEZA CHAT ID IRI GUSOMWA ---
active_user = __streamlit__.session_state.logged_in_user
if active_user:
    if active_user not in __streamlit__.session_state.chats:
        __streamlit__.session_state.chats[active_user] = {}
    
    if not __streamlit__.session_state.current_chat_id or __streamlit__.session_state.current_chat_id not in __streamlit__.session_state.chats[active_user]:
        if __streamlit__.session_state.chats[active_user]:
            __streamlit__.session_state.current_chat_id = list(__streamlit__.session_state.chats[active_user].keys())[0]
        else:
            init_id = f"chat_{int(time.time())}"
            __streamlit__.session_state.chats[active_user][init_id] = {
                "title": "New Chat",
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}]
            }
            __streamlit__.session_state.current_chat_id = init_id

    current_chat_id = __streamlit__.session_state.current_chat_id
    user_messages_list = __streamlit__.session_state.chats[active_user][current_chat_id]["messages"]

    # --- 6. KWEREKANA UBUSOBANURO BW'IBIGANIRO (CHAT MESSAGES DISPLAY) ---
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

    # --- 7. FILE UPLOADER ---
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

    # --- 8. CHAT INPUT & GROQ HANDLER ---
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
        
        # Hindura Title ya chat niba yari "New Trust/New Chat" ikaba ubutumwa bwa mbere bwa user
        if __streamlit__.session_state.chats[active_user][current_chat_id]["title"] == "New Chat":
            __streamlit__.session_state.chats[active_user][current_chat_id]["title"] = ikibazo

        __streamlit__.session_state.chats[active_user][current_chat_id]["messages"].append(full_user_message)
        
        try:
            with __streamlit__.spinner("GKevin is thinking....."):
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=__streamlit__.session_state.chats[active_user][current_chat_id]["messages"],
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
                
            __streamlit__.session_state.chats[active_user][current_chat_id]["messages"].append({"role": "assistant", "content": igisubizo_cya_ai})
            __streamlit__.rerun()
            
        except Exception as e:
            __streamlit__.error(f"Haba habaye ikibazo: {e}")
