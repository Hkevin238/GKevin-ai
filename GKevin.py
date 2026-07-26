import streamlit as __streamlit__
from openai import OpenAI

# 1. Gushiraho Title na Layout y'urupapuro
__streamlit__.set_page_config(
    page_title="GKevin AI",
    page_icon="kvn.png", # <-- Iyi ni logo y'akato kuri tab ya browser
    layout="centered"
)

# =================== GUSHYIRA LOGO NINI HAGATI ===================
col1, col2, col3 = __streamlit__.columns([1,2,1]) # Dukoresha 3 columns kuyishyira hagati
with col2:
    __streamlit__.image("kvn.png", width=180) # <-- IYI N'IFOTO NINI YA LOGO
# =================================================================

__streamlit__.title("GKevin AI Assistant") # Nakuweho emoji kuko dusanganywe logo
__streamlit__.write("I'M A NEW AI GENERATION designed BY Kevin ")

# 2. Guhuza na Groq API
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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"
)

# 3. Kubika amateka y'ibiganiro muri Streamlit Session State
if "messages_historike" not in __streamlit__.session_state:
    __streamlit__.session_state.messages_historike = [
        {
            "role": "system", 
            "content": "I'm GKevin AI, an ultra-fast assistant created by Developer Kevin on July 25, 2026, at the afternoon.For
