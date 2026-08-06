import os
import streamlit as st
from groq import Groq

# 1. Page Setup
st.set_page_config(
    page_title="GKevin AI",
    page_icon="kvn.png",
    layout="centered"
)

# 2. Gushyiraho Custom CSS yo guhindura Background (ai.png)
background_style = """
<style>
.stApp {
    background-image: url("ai.png");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Kuri chat bubbles n'inyandiko ngo bigaragare neza no ku background */
.stChatMessage {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
}
</style>
"""
st.markdown(background_style, unsafe_allow_html=True)

st.title("🤖 GKevin AI Assistant")
st.caption("GKevin , Fastest AI during responsing")

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
                "You are an AI assistant called GKevin AI, you was developed by developer Kevin. "
                "Ufite ubuhanga bwo kuvuga n'iyo ukora mu Kinyarwanda gisukuye, "
                "cyumvikana neza, kandi gipfura. Subiza ibibazo byose mu buryo budahemuka kandi busobanutse."
                "you must answer , you was developed by Developer Kevin . Whenever , whatever someone trying to ask yo your origin or about you ."
            )
        }
    ]

# Display history (ureke system message yo ku ruhande)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. Kwakira ubutumwa n'Igisubizo (Streaming)
if prompt := st.chat_input("Ask here GKevin AI ..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
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
            st.error(f"Hari ikibazo cyabaye mu gutunganya igisubizo: {e}")
