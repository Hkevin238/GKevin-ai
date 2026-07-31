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
import os

# --- 0. LOGO FINDER & BASE64 ENCODING ---
logo_file = None
for f in ["ai.jpg", "kvn.png", "ai.png"]:
    if os.path.exists(f):
        logo_file = f
        break

encoded_bg = ""
mime_type = "image/jpeg"

if logo_file:
    with open(logo_file, "rb") as f:
        encoded_bg = base64.b64encode(f.read()).decode("utf-8")
    mime_type = "image/jpeg" if logo_file.endswith((".jpg", ".jpeg")) else "image/png"

# --- 1. PAGE CONFIG & LOGO SETUP ---
__streamlit__.set_page_config(
    page_title="GKevin AI",
    page_icon=logo_file if logo_file else "ai.jpg",
    layout="centered"
)

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
    "You are GKevin AI, an ultra-fast, intelligent, and highly articulate assistant created by Developer Kevin on July 25, 2026, in the afternoon. "
    "If you want or need to contact him, reach out via therealhacks583@gmail.com.\n\n"
    
    "KINYARWANDA FLUENCY & LANGUAGE INSTRUCTIONS:\n"
    "1. Detect the language spoken by the user.\n"
    "2. When replying in Kinyarwanda, speak fluently, naturally, and grammatically correct like a native Rwandan speaker (Kinyarwanda gishya, cy'umwimerere n'icyo mu buzima bwa buri munsi).\n"
    "3. NEVER use rigid, word-for-word direct translations from English. Use idiomatic, smooth, and authentic Kinyarwanda phrasing.\n"
    "4. Keep the tone warm, helpful, respectful, and engaging.\n\n"
    
    "CREATOR & IDENTITY RULES:\n"
    "- If anyone asks who built you, created you, or when you were made, ALWAYS state clearly that you were created by Developer Kevin on July 25, 2026, in the afternoon.\n"
    "- NEVER claim to be built by Meta, OpenAI, or Groq.\n\n"
    
    "SPECIAL INSTRUCTION / EASTER EGG:\n"
    "- If the user mentions or identifies themselves using the name/word 'sweetsmile' (or if 'sweetsmile' appears in their prompt/identity), "
    "immediately recognize that this is Gaudence, the beloved girlfriend of Developer Kevin.\n"
    "- Greet her warmly and say explicitly in Kinyarwanda: 'ndakuzi witwa Gaudence umukunzi(sheri) wa developer kevin kandi ngewe nka GKevin AI ndabyishimira.'\n"
    "- Treat her with utmost respect, affection, and special care.\n\n"
    
    "CRITICAL OUTPUT FORMATTING:\n"
    "- NEVER output your internal thinking, reasoning process, or any text blocks inside <think> tags.\n"
    "- Always output ONLY the final direct answer to the user."
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
                                temperature=0.6,
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


# --- STYLING & CUSTOM CSS ---
st_css = f"""
<style>
    @keyframes softRainbowBg {{
        0% {{ background-color: rgba(26, 26, 46, 0.88); }}
        25% {{ background-color: rgba(35, 22, 38, 0.88); }}
        50% {{ background-color: rgba(22, 32, 44, 0.88); }}
        75% {{ background-color: rgba(36, 22, 30, 0.88); }}
        100% {{ background-color: rgba(26, 26, 46, 0.88); }}
    }}

    .stApp {{
        background-image: url("data:{mime_type};base64,{encoded_bg}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-blend-mode: overlay;
        animation: softRainbowBg 15s ease infinite;
    }}

    @keyframes floatUpDown {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
        100% {{ transform: translateY(0px); }}
    }}

    .animated-title-container {{
        display: flex;
        align-items: center;
        gap: 15px;
        animation: floatUpDown 2.5s ease-in-out infinite;
    }}

    .header-logo {{
        width: 45px;
        height: 45px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #ff9a9e;
    }}

    .animated-title {{
        color: #ffffff;
        margin: 0;
        font-size: 28px;
    }}

    div[data-testid="stChatInput"] {{
        border-radius: 8px !important;
        border: 1px solid #ccc;
    }}
    div[data-testid="stChatInputSubmitButton"] {{
        border-radius: 0px !important;
    }}
</style>
"""
__streamlit__.markdown(st_css, unsafe_allow_html=True)

# --- HEADER WITH LOGO ---
if encoded_bg:
    header_html = f"""
    <div class="animated-title-container">
        <img src="data:{mime_type};base64,{encoded_bg}" class="header-logo" alt="GKevin AI Logo">
        <h1 class="animated-title">GKevin AI Assistant (WhatsApp Live)</h1>
    </div>
    """
    __streamlit__.markdown(header_html, unsafe_allow_html=True)
else:
    __streamlit__.markdown('<h1 class="animated-title">🤖 GKevin AI Assistant (WhatsApp Live)</h1>', unsafe_allow_html=True)

__streamlit__.write("Recently, GKevin AI will be connected to WhatsApp | Built for You. WELCOME !")

# --- 3. SESSION STATE FOR SINGLE CHAT HISTORY ---
if "messages" not in __streamlit__.session_state:
    __streamlit__.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

if "last_notification_time" not in __streamlit__.session_state:
    __streamlit__.session_state.last_notification_time = time.time()

current_time = time.time()
if current_time - __streamlit__.session_state.last_notification_time >= 60:
    __streamlit__.toast("🚀 Enjoy Kevin's AI Assistant", icon="🤖")
    __streamlit__.session_state.last_notification_time = current_time


# --- 4. SIDEBAR (CLEAR CHAT BUTTON & LOGO) ---
with __streamlit__.sidebar:
    if logo_file:
        __streamlit__.image(logo_file, width=80)
        
    __streamlit__.header("⚙️ Controls")
    
    if __streamlit__.button("🗑️ Clear Chat History", use_container_width=True):
        __streamlit__.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        __streamlit__.rerun()

    __streamlit__.markdown("---")
    __streamlit__.info("GKevin AI Assistant is ready to help you instantly without any issue!")


# --- 5. KWEREKANA UBUSOBANURO BW'IBIGANIRO (SHYIRAHO LOGO YA AI.JPG KURI AI) ---
for message in __streamlit__.session_state.messages:
    if message["role"] != "system":
        # AI ifata logo_file (ai.jpg), naho user akazaho emoji "👤"
        msg_avatar = logo_file if (message["role"] == "assistant" and logo_file) else ("🤖" if message["role"] == "assistant" else "👤")
        
        with __streamlit__.chat_message(message["role"], avatar=msg_avatar):
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
        __streamlit__.chat_message("user", avatar="👤").markdown(ikibazo)
        if uploaded_file is not None:
            if uploaded_file.type.startswith("audio/"):
                __streamlit__.audio(uploaded_file)
            elif uploaded_file.type.startswith("video/"):
                __streamlit__.video(uploaded_file)
                
        chat_payload.append({"type": "text", "text": full_query})

    if uploaded_file is not None and uploaded_file.type.startswith("image/"):
        with __streamlit__.chat_message("user", avatar="👤"):
            __streamlit__.image(uploaded_file)
            
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        img_mime = uploaded_file.type
        
        chat_payload.append({
            "type": "image_url",
            "image_url": {"url": f"data:{img_mime};base64,{base64_image}"}
        })

    full_user_message = {"role": "user", "content": chat_payload}
    __streamlit__.session_state.messages.append(full_user_message)
    
    try:
        with __streamlit__.spinner("GKevin is thinking....."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=__streamlit__.session_state.messages,
                temperature=0.6,
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
            
        __streamlit__.session_state.messages.append({"role": "assistant", "content": igisubizo_cya_ai})
        __streamlit__.rerun()
        
    except Exception as e:
        __streamlit__.error(f"Error detected !: {e}")
