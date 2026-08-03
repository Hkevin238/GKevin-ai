import streamlit as st
from openai import OpenAI
import base64
import os

# --- 1. LOGO FINDER & BASE64 ENCODING ---
logo_file = None
for f in ["ai.jpg", "kvn.png", "ai.png"]:
    if os.path.exists(f):
        logo_file = f
        break

encoded_bg = ""
mime_type = "image/jpeg"

if logo_file:
    try:
        with open(logo_file, "rb") as f:
            encoded_bg = base64.b64encode(f.read()).decode("utf-8")
        mime_type = "image/jpeg" if logo_file.endswith((".jpg", ".jpeg")) else "image/png"
    except Exception:
        pass

# --- 2. PAGE CONFIG ---
st.set_page_config(
    page_title="GKevin AI",
    page_icon=logo_file if logo_file else "🤖",
    layout="centered"
)

# --- 3. GROQ API INTEGRATION ---
try:
    groq_api_key_val = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key_val = "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"

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key_val
)

MODEL_NAME = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "You are GKevin AI, an ultra-fast, highly intelligent, articulate, and friendly AI assistant created by Developer Kevin on July 25, 2026, in the afternoon. "
    "If anyone needs or wants to contact Developer Kevin directly, provide his official email: therealhacks583@gmail.com.\n\n"
    "ADVANCED KINYARWANDA FLUENCY & LANGUAGE RULES:\n"
    "1. When the user writes in Kinyarwanda, reply ONLY in natural, native, and grammatically precise Kinyarwanda.\n"
    "2. STRICTLY AVOID word-for-word direct translations from English or direct robotic/Google-translated phrasing.\n"
    "3. Use authentic, smooth, modern Rwandan sentence structures (Ikinyarwanda gishya n'icy'umwimerere cy'i Rwanda).\n"
    "4. Ensure correct noun-class agreements, natural verb conjugations, and fluent transitions.\n"
    "5. Always match the tone: polite, intelligent, warm, respectful, and engaging.\n\n"
    "CRITICAL OUTPUT FORMATTING:\n"
    "- NEVER output your internal thinking, reasoning process, or any text blocks inside <think> tags.\n"
    "- Always output ONLY the final direct answer to the user."
)

# --- 4. CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- DISPLAY MESSAGES ---
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = logo_file if (message["role"] == "assistant" and logo_file) else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# --- CHAT INPUT & GROQ API CALL ---
if ikibazo := st.chat_input("Type here...."):
    st.session_state.messages.append({"role": "user", "content": ikibazo})
    
    with st.chat_message("user"):
        st.markdown(ikibazo)
        
    try:
        with st.spinner("GKevin is thinking....."):
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                temperature=0.5,
                top_p=0.9,
                max_tokens=1024
            )
            
            igisubizo_cya_ai = completion.choices[0].message.content
            
            if "</think>" in igisubizo_cya_ai:
                igisubizo_cya_ai = igisubizo_cya_ai.split("</think>")[-1].strip()
            igisubizo_cya_ai = igisubizo_cya_ai.replace("<think>", "").replace("</think>", "").strip()
            
            st.session_state.messages.append({"role": "assistant", "content": igisubizo_cya_ai})
            st.rerun()
            
    except Exception as e:
        st.error(f"Error detected: {e}")
