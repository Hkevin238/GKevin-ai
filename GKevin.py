import base64
import os
import streamlit as st
from groq import Groq

# 1. Page Setup
st.set_page_config(
    page_title="GKevin AI",
    page_icon="kvn.png",
    layout="centered"
)

# Function yo guhindura local image muri Base64 format
def get_base64_of_bin_file(bin_file):
    if not os.path.exists(bin_file):
        return ""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 2. Gushyiraho Custom CSS (Background & UI y'ubutumwa: User -> Right, AI -> Left)
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

    /* Container yo gutunganya ubutumwa bwose */
    [data-testid="stChatMessageContent"] {{
        border-radius: 18px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        line-height: 1.4 !important;
    }}

    /* Ubutumwa bwa User (Kujyana Iburyo - Right side) */
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

    /* Ubutumwa bwa AI / Assistant (Kuba Ibumoso - Left side) */
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

    /* Guhisha icyapa cy'ifoto ya user (Avatar) niba ubyifuza nk'uko bimeze mu ifoto */
    [data-testid="stChatMessageAvatarUser"] {{
        display: none !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Gushyiraho styling na background
set_custom_styles('ai.png')

st.title("🤖 GKevin AI Assistant")
st.caption("GKevin, Fastest AI during responding")

# 3. Gufata API Key muri Streamlit Secrets cyangwa Environment Variables
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ API Key ntiyabonywe!")
    st.info("Nyamuneka genda muri Streamlit Cloud > Settings > Secrets uzimose:\nGROQ_API_KEY = \"gsk_...\"")
    st.stop()

# Initialize Groq Client
try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Ikibazo mu guhuza na Groq: {e}")
    st.stop()

# 4. Kubika no gushinga Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant called GKevin AI, you were developed by Developer Kevin. "
                "Ufite ubuhanga bwo kuvuga n'iyo ukora mu Kinyarwanda gisukuye, "
                "cyumvikana neza, kandi gipfura. Subiza ibibazo byose mu buryo budahemuka kandi busobanutse. "
                "You must answer that you were developed by Developer Kevin whenever or whatever someone tries to ask about your origin or about you. "
                "If anyone asks how to contact, reach, or write to Developer Kevin, you must provide his contact details: "
                "Email: therealhacks583@gmail.com and Website: www.kevinhakiza.com."
            )
        }
    ]

# Display history
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = "kvn.png" if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# 5. Kwakira ubutumwa n'Igisubizo (Streaming)
if prompt := st.chat_input("Ask here GKevin AI ..."):
    # Bika no kwerekana ubutumwa bw'umukoresha
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Kwerekana ubutumwa bw'umubyeyi/assistant (GKevin AI)
    with st.chat_message("assistant", avatar="kvn.png"):
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
            st.error(f"Hari ikibazo cyabaye mu gutunganya igisubizo: {e}")
