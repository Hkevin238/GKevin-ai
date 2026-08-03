import streamlit as __streamlit__
import streamlit.components.v1 as components
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

# --- 1. DIRECT DOWNLOAD LINK YA APK ---
APK_DIRECT_LINK = "https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_HERE"

# --- 2. LOGO FINDER & BASE64 ENCODING ---
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

# --- 3. PAGE CONFIG ---
__streamlit__.set_page_config(
    page_title="GKevin AI",
    page_icon=logo_file if logo_file else "🤖",
    layout="centered"
)

# --- WHATSAPP PRODUCTION CREDENTIALS ---
WHATSAPP_PHONE_NUMBER_ID = "1227756223755507"
WHATSAPP_BUSINESS_ACCOUNT_ID = "1186592933667697"
WHATSAPP_PHONE = "+1 (555) 664-6865"
WEBHOOK_VERIFY_TOKEN = "gkevin_verify_token_123"
WHATSAPP_ACCESS_TOKEN = "3GtWP41MHsU58iGAD61xtD42gjn_5zujVmnszLcxX2EJ1MgWm"

# --- GROQ API INTEGRATION ---
try:
    groq_api_key_val = __streamlit__.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key_val = "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"

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key_val
)

MODEL_NAME = "mixtral-8x7b-32768"

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

# --- CHAT INPUT & GROQ HANDLER ---
if ikibazo := __streamlit__.chat_input("Type here...."):
    __streamlit__.session_state.messages.append({"role": "user", "content": ikibazo})
    
    # Tubakire amashusho nk'inyandiko gusa kuko Mixtral itagira Vision:
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in __streamlit__.session_state.messages:
        if msg["role"] != "system":
            # Gukuramo ibintu byose bishyira amashusho muri API call
            if isinstance(msg["content"], list):
                text_only = ""
                for item in msg["content"]:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_only += item.get("text", "")
                api_messages.append({"role": msg["role"], "content": text_only})
            else:
                api_messages.append({"role": msg["role"], "content": str(msg["content"])})

    try:
        with __streamlit__.spinner("GKevin is thinking....."):
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=api_messages,
                temperature=0.5,
                top_p=0.9,
                max_tokens=1024
            )
            
            igisubizo_cya_ai = completion.choices[0].message.content
            __streamlit__.session_state.messages.append({"role": "assistant", "content": igisubizo_cya_ai})
            __streamlit__.rerun()
            
    except Exception as e:
        __streamlit__.error(f"Error detected !: {e}")
