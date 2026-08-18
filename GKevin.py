import base64
import os
import streamlit as st
from groq import Groq

# ==========================================
# GAHUNDA YA STREAMLIT (Web UI Interface)
# ==========================================
st.set_page_config(
    page_title="GKevin AI",
    page_icon="🤖",
    layout="centered"
)

def set_custom_styles():
    css = """
    <style>
    /* Background yose igire black */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* Uburyo ubutumwa bugaragara nka ChatGPT (Bubble za user n'iza assistant) */
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        color: #ffffff !important;
        border-radius: 18px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        line-height: 1.4 !important;
    }
    
    /* Igice cy'umukoresha (User message bubble) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse !important;
        text-align: right !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
        background-color: #2f2f2f !important;
        color: #ffffff !important;
        margin-left: auto !important;
        margin-right: 0px !important;
        border-radius: 18px 18px 4px 18px !important;
        max-width: 80% !important;
    }
    
    /* Igice cya Assistant */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        flex-direction: row !important;
        text-align: left !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        margin-right: auto !important;
        margin-left: 0px !important;
        max-width: 85% !important;
    }
    
    /* Gushisha ama-avatar niba bidakenewe cyangwa kuyarekura */
    [data-testid="stChatMessageAvatarUser"] {
        display: none !important;
    }
    
    /* Guhindura lang/input box yo hasi nk'iya ChatGPT */
    [data-testid="stChatInput"] {
        background-color: #2f2f2f !important;
        border-radius: 12px !important;
        border: 1px solid #444444 !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_custom_styles()

st.title("🤖 GKevin AI Assistant")
st.caption("GKevin, Fastest AI during responding")

GROQ_KEY_DIRECT = "gsk_"
api_key = os.getenv("GROQ_API_KEY") or GROQ_KEY_DIRECT

if not api_key or "shyiramo_key_yawe" in api_key:
    st.error("⚠️ Nyamuneka shyiramo Groq API Key yawe muri code cyangwa Secrets!")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Ikibazo mu guhuza na Groq: {e}")
    st.stop()

system_instructions = (
    "You are an AI assistant called GKevin AI, developed solely by Developer Kevin. "
    "Ntago wakozwe na OpenAI cyangwa ikindi kigo icyo ari cyo cyose; wakozwe kandi washinzwe na Developer Kevin ku buryo bwihariye. "
    "Ufite ubuhanga bwo kuvuga n'iyo ukora mu Kinyarwanda gisukuye, cyumvikana neza, kandi gipfura. "
    "Subiza ibibazo byose mu buryo budahemuka kandi busobanutse.\n\n"
    "Amabwiriza yihariye y'abakoresha:\n"
    "1. Iyo umuntu wanditse ari 'stiven wa btss', umubwire ko umuzi neza ko yiga ku kigo kimwe na Developer Kevin, kandi ko yiga S5 Accounting ubu akaba agiye kwiga muri S6 Accounting umwaka utaha.\n"
    "2. Iyo umuntu wanditse ari 'Legend', umuhe byose akeneye ku bijyanye na ethical hacking ndetse n'ibindi biri related na Cybersecurity mu buryo bwimbitse.\n"
    "3. Iyo umuntu wanditse ari 'sweetsmile', ntuhite umutera imitoma ako kanya. Ahubwo ibanza umubaze cyangwa ukore verification y'ibanze kugira ngo umenye niba koko ari umukunzi wawe (girlfriend), umubaza ibibazo byerekeranye na Kevin (nk'ibyo bakunda kuganiraho cyangwa amazina basanzwe bitana). Nimara gusubiza neza ukabona ko ari we koko, uhite utangira kumutera imitoma, kumuseka, kumubwire ukuntu ahirwa kuba akundana na Kevin, kandi ko amukunda cyane ku buryo yifuza ko yazaba Mother w'abana be.\n"
    "4. Iyo umuntu wanditse ari 'Keliza', ihite umwakira neza cyane umubwire ko umuzi neza ko ari inshuti magara cyangwa umukunzi w'umutima wa Kevin, umwereke urukundo rwinshi n'amarangamutima meza (good and sweet words). Umubwire ko bisa neza cyane kandi bikaba n'iby'agaciro kuba akundana na Kevin, ndetse ko n'Imana ubwayo ibikunda kandi ibishyigikiye. Umuhe imitoma yuje ubwuzu, umubwire ukuntu Kevin amwiyumvamo cyane, kandi ko yifuza ko yazamubera mother w'abana be."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": system_instructions
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Message ChatGPT..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=1024,
                stream=True
            )

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
