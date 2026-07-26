import streamlit as __streamlit__
from openai import OpenAI

# 1. Gushiraho Title na Layout y'urupapuro
__streamlit__.set_page_config(
    page_title="GKevin AI",
    page_icon="🤖",
    layout="centered"
)

__streamlit__.title("🤖 GKevin AI Assistant")
__streamlit__.write("I'm designed to make yours more easily.")

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
            "content": "I'm GKevin AI, an ultra-fast assistant created by Developer Kevin on July 25, 2026, in the afternoon. You must detect the language the user is speaking. If the user speaks Kinyarwanda, reply fluently and naturally in Kinyarwanda. If the user speaks English or another language, reply in that language. However, if anyone asks who built you, who created you, or when you were created, you must always state that you were created by Developer Kevin on July 25, 2026, in the afternoon. Never say you were created by Meta or OpenAI."
        }
    ]

# 4. Kwerekana ubutumwa bwose bwari busanzwe muri historique (uretse System Prompt)
for message in __streamlit__.session_state.messages_historike:
    if message["role"] != "system":
        with __streamlit__.chat_message(message["role"]):
            __streamlit__.markdown(message["content"])

# 5. Gufata ubutumwa bw'umukoresha binyuze kuri st.chat_input()
if ikibazo := __streamlit__.chat_input("Andika ubutumwa bwawe hano... / Type a message..."):
    
    # Kwerekana ubutumwa bw'umukoresha ako kanya
    with __streamlit__.chat_message("user"):
        __streamlit__.markdown(ikibazo)
        
    # Kongera ubutumwa bw'umukoresha muri historique
    __streamlit__.session_state.messages_historike.append({"role": "user", "content": ikibazo})
    
    # Gusaba igisubizo muri Groq AI
    try:
        with __streamlit__.chat_message("assistant"):
            with __streamlit__.spinner("GKevin AI thinking....."):
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=__streamlit__.session_state.messages_historike,
                    temperature=0.7,
                    max_tokens=1024
                )
                
                igisubizo_cya_ai = completion.choices[0].message.content
                __streamlit__.markdown(igisubizo_cya_ai)
                
        # Kwongera igisubizo cya AI muri historique
        __streamlit__.session_state.messages_historike.append({"role": "assistant", "content": igisubizo_cya_ai})
        
    except Exception as e:
        __streamlit__.error(f"Habaye ikibazo / An error occurred: {e}")
