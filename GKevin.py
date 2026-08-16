import base64
import os
import threading
from flask import Flask, request, jsonify
import streamlit as st
from groq import Groq

# ==========================================
# 1. GAHUNDA YA FLASK (Backend yo kwakira ubutumwa na Verification)
# ==========================================
app = Flask(__name__)

# Verify Token igomba guhura neza n'iyo wandika kuri Meta
VERIFY_TOKEN = "gkevin-ai@0793868332"
WHATSAPP_TARGET_PHONE = os.getenv("WHATSAPP_PHONE", "+250732463273")

@app.route('/whatsapp-webhook', methods=['GET', 'POST'])
def whatsapp_webhook():
    # 1. Kwakira GET request (Iyo Meta igenzura kandi ikemeza Webhook)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("WEBHOOK_VERIFIED")
                return challenge, 200
            else:
                return jsonify({"error": "Verification failed"}), 403
        return jsonify({"error": "Invalid request"}), 400

    # 2. Kwakira POST request (Ubutumwa busanzwe bw'abakiriya)
    data = request.json
    try:
        incoming_msg = data.get('message', '')
        sender_phone = data.get('phone', WHATSAPP_TARGET_PHONE)
        
        if incoming_msg:
            api_key = os.getenv("GROQ_API_KEY") or "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"
            if api_key and "shyiramo_key_yawe" not in api_key:
                groq_client = Groq(api_key=api_key)
                completion = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an AI assistant called GKevin AI, developed by Developer Kevin. "
                                "Ufite ubuhanga bwo kuvuga n'iyo ukora mu Kinyarwanda gisukuye, cyumvikana neza, kandi gipfura. "
                                "Subiza ibibazo byose mu buryo budahemuka kandi busobanutse."
                            )
                        },
                        {"role": "user", "content": incoming_msg}
                    ],
                    temperature=0.7,
                    max_tokens=1024
                )
                ai_reply = completion.choices[0].message.content
                
                # Hano ushobora kongeramo uburyo bwa API (nka WhatsApp Cloud API) 
                # bwo kohereza 'ai_reply' kuri sender_phone igihe ubikeneye.
                print(f"Igisubizo cya GKevin AI kuri {sender_phone}: {ai_reply}")
                
    except Exception as e:
        print(f"Ikibazo cyabaye: {e}")
        
    return jsonify({"status": "success"}), 200

def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

if "flask_running" not in st.session_state:
    st.session_state.flask_running = True
    threading.Thread(target=run_flask, daemon=True).start()


# ==========================================
# 2. GAHUNDA YA STREAMLIT (Web UI Interface)
# ==========================================
st.set_page_config(
    page_title="GKevin AI",
    page_icon="ai.jpg",
    layout="centered"
)

def get_base64_of_bin_file(bin_file):
    if not os.path.exists(bin_file):
        return ""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_custom_styles(main_bg):
    bg_style = ""
    if os.path.exists(main_bg):
        bin_str = get_base64_of_bin_file(main_bg)
        bg_style = f"""
            background-image: url("data:image/jpeg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        """

    css = f"""
    <style>
    .stApp {{
        {bg_style}
    }}
    [data-testid="stChatMessageContent"] {{
        border-radius: 18px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        line-height: 1.4 !important;
    }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        flex-direction: row-reverse !important;
        text-align: right !important;
    }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {{
        background-color: #2f2f2f !important;
        color: #ffffff !important;
        margin-left: auto !important;
        margin-right: 0px !important;
        border-radius: 18px 18px 4px 18px !important;
        max-width: 80% !important;
    }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
        flex-direction: row !important;
        text-align: left !important;
    }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {{
        background-color: transparent !important;
        color: #ffffff !important;
        margin-right: auto !important;
        margin-left: 0px !important;
        border-radius: 18px 18px 18px 4px !important;
        max-width: 85% !important;
    }}
    [data-testid="stChatMessageAvatarUser"] {{
        display: none !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_custom_styles('ai.jpg')

st.title("🤖 GKevin AI Assistant")
st.caption("GKevin, Fastest AI during responding")

GROQ_KEY_DIRECT = "gsk_"
api_key = os.getenv("GROQ_API_KEY") or GROQ_KEY_DIRECT

if not api_key or "shyiramo_key_yawe" in api_key:
    st.error("⚠️ Nyamuneka shyiramo Groq API Key yawe muri code hejuru aho yagenewe!")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Ikibazo mu guhuza na Groq: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant called GKevin AI, developed by Developer Kevin. "
                "Ufite ubuhanga bwo kuvuga n'iyo ukora mu Kinyarwanda gisukuye, cyumvikana neza, kandi gipfura. "
                "Subiza ibibazo byose mu buryo budahemuka kandi busobanutse."
            )
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = "ai.jpg" if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask here GKevin AI ..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="ai.jpg"):
        message_placeholder = st.empty()

        try:
            with st.status("GKevin AI thinking....", expanded=False) as status:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=1024,
                    stream=True
                )
                status.update(label="Done!", state="complete", expanded=False)

            full_response = ""
            for chunk in completion:
                chunk_content = chunk.choices[0].delta.content or ""
                full_response += chunk_content
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            message_placeholder.empty()
            st.error(f"Hari ikibazo cyabaye: {e}")
