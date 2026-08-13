import base64
import os
import streamlit as st
import google.generativeai as genai

# 1. Page Setup
st.set_page_config(
    page_title="GKevin AI",
    page_icon="kvn.png",
    layout="centered"
)

# Function yo guhindura local image muri Base64 format
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 2. Gushyiraho Custom CSS
def set_custom_styles(main_bg):
    bg_style = ""
    if os.path.exists(main_bg):
        bin_str = get_base64_of_bin_file(main_bg)
        bg_style = f"""
            background-image: url("data:image/png;base64,{bin_str}");
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

set_custom_styles('ai.png')

st.title("🤖 GKevin AI Assistant")
st.caption("GKevin, Powered by Gemini AI")

# 3. Gufata Google API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API Key ntiyabonywe!")
    st.info("Nyamuneka genda muri Streamlit Cloud > Settings > Secrets uzimose:\nGEMINI_API_KEY = \"AIzaSy...\"")
    st.stop()

# Initialize Gemini Client
try:
    genai.configure(api_key=api_key)
    # Gukoresha model ya gemini-1.5-flash cyangwa se gemini-2.5-flash
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "You are an AI assistant called GKevin AI, you were developed by Developer Kevin. "
            "Ufite ubuhanga bwo kuvuga n'iyo ukora mu Kinyarwanda gisukuye, "
            "cyumvikana neza, kandi gipfura. Subiza ibibazo byose mu buryo budahemuka kandi busobanutse. "
            "You must answer that you were developed by Developer Kevin whenever or whatever someone tries to ask about your origin or about you. "
            "If anyone asks how to contact, reach, or write to Developer Kevin, you must provide his contact details: "
            "Email: therealhacks583@gmail.com and Website: www.kevinhakiza.com."
        )
    )
except Exception as e:
    st.error(f"Ikibazo mu guhuza na Gemini: {e}")
    st.stop()

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    avatar = "kvn.png" if message["role"] == "model" else None
    with st.chat_message("assistant" if message["role"] == "model" else "user", avatar=avatar):
        st.markdown(message["parts"][0])

# 5. Kwakira ubutumwa n'Igisubizo (Streaming)
if prompt := st.chat_input("Ask here GKevin AI ..."):
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="kvn.png"):
        message_placeholder = st.empty()
        
        try:
            # Guhindura uburyo amateka y'ibiganiro yoherezwa muri Gemini format
            chat_history = [
                {"role": m["role"], "parts": m["parts"]} 
                for m in st.session_state.messages[:-1]
            ]
            
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(prompt, stream=True)

            full_response = ""
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "model", "parts": [full_response]})

        except Exception as e:
            message_placeholder.empty()
            st.error(f"Hari ikibazo cyabaye mu gutunganya igisubizo: {e}")
