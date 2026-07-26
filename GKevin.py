import streamlit as __streamlit__
from openai import OpenAI
import base64
from PIL import Image
import io

# --- Gushyira ho CSS ya ChatGPT-like input box ---
# Iyi CSS ikoresha st.markdown kugira ngo ihindure imiterere y'agakupa k'inyandiko
st_css = """
<style>
    /* Gukora ngo input box igororoke (square edges) nkiya ChatGPT */
    div[data-testid="stChatInput"] {
        border-radius: 8px !important; /* Hano niho hagena ubugororotsi */
        border: 1px solid #ccc;
    }
    /* Gukuraho 'rounded corners' kuri button yayo */
    div[data-testid="stChatInputSubmitButton"] {
        border-radius: 0px !important;
    }
</style>
"""
__streamlit__.markdown(st_css, unsafe_allow_html=True)


# 1. Gushiraho Title na Layout y'urupapuro
__streamlit__.set_page_config(
    page_title="GKevin AI",
    page_icon="🤖",
    layout="centered"
)

__streamlit__.title("🤖 GKevin AI Assistant (Vision)")
__streamlit__.write("I'm designed to make yours more easily.")

# --- 2.ONGERA UBUKOZI BW'IFOTO: Guhuza na Groq API (Koresha model ya vision) ---
# Wintege ko nshyizemo model nshya "llava-v1.5-7b-4096-preview" kugira ngo ifoto isomeke.
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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"
)

# 3. Kubika amateka y'ibiganiro muri Streamlit Session State
if "messages_historike" not in __streamlit__.session_state:
    __streamlit__.session_state.messages_historike = [
        {
            "role": "system", 
            "content": "I'm GKevin AI, an ultra-fast assistant created by Developer Kevin on July 25, 2026, at the afternoon. You must detect the language the user is speaking. If the user speaks Kinyarwanda, reply fluently and naturally in Kinyarwanda. If the user speaks English or another language, reply in that language. If you are provided with an image, describe what is in the image in the language the user is currently using or requested."
        }
    ]

# 4. Sidebar History (Nta gihindutse hano)
with __streamlit__.sidebar:
    __streamlit__.header("💬 Chat History")
    
    if __streamlit__.button("Clear Conversation"):
        __streamlit__.session_state.messages_historike = [
            __streamlit__.session_state.messages_historike[0]
        ]
        __streamlit__.rerun()

    __streamlit__.markdown("---")
    
    # --- 4b.ONGEYEHO: File Uploader muri Sidebar ---
    __streamlit__.subheader("🖼️ Attach an Image (Optional)")
    uploaded_file = __streamlit__.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    
    # Kwerekana ifoto yashyizemo
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        __streamlit__.image(image, caption="Uploaded Image", use_column_width=True)

# 5. Kwerekana ubutumwa bwose bwari busanzwe muri historique
for message in __streamlit__.session_state.messages_historike:
    if message["role"] != "system":
        with __streamlit__.chat_message(message["role"]):
            # Hano dukuramo content niba ari dictionary cyangwa string (kubera ko ifoto na text biba bitandukanye)
            content = message['content']
            if isinstance(content, list):
                for item in content:
                    if item['type'] == 'text':
                        __streamlit__.markdown(item['text'])
                    elif item['type'] == 'image_url':
                        __streamlit__.image(item['image_url']['url'])
            else:
                __streamlit__.markdown(content)

# 6. Gufata ubutumwa bw'umukoresha
if ikibazo := __streamlit__.chat_input("Andika ubutumwa hano... / Type a message..."):
    
    # Kwitegura kohereza (message payload)
    chat_payload = []
    
    # --- Ongeramo Text niba ihari ---
    if ikibazo:
        __streamlit__.chat_message("user").markdown(ikibazo)
        chat_payload.append({"type": "text", "text": ikibazo})

    # --- 6b.ONGERA UBUKOZI BW'IFOTO: Hindura ifoto muri Base64 niba ihari ---
    if uploaded_file is not None:
        # Kwerekana ifoto mu butumwa bw'umukoresha
        with __streamlit__.chat_message("user"):
            __streamlit__.image(uploaded_file)
            
        # Guhindura ifoto muri Base64 ngo Groq iyisome
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        mime_type = uploaded_file.type
        
        # Kongera ifoto muri payload yoherezwa
        chat_payload.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
        })

    # Kongera ubutumwa bw'umukoresha (hamwe n'ifoto niba ihari) muri historique
    full_user_message = {"role": "user", "content": chat_payload}
    __streamlit__.session_state.messages_historike.append(full_user_message)
    
    # Gusaba igisubizo muri Groq AI (Version model)
    try:
        with __streamlit__.chat_message("assistant"):
            with __streamlit__.spinner("GKevin AI thinking....."):
                completion = client.chat.completions.create(
                    # Iyi model ya LLAVA niyo ishobora vision kuri Groq
                    model="llava-v1.5-7b-4096-preview", 
                    messages=__streamlit__.session_state.messages_historike,
                    temperature=0.7,
                    max_tokens=1024
                )
                
                igisubizo_cya_ai = completion.choices[0].message.content
                __streamlit__.markdown(igisubizo_cya_ai)
                
        # Kwongera igisubizo cya AI muri historique
        __streamlit__.session_state.messages_historike.append({"role": "assistant", "content": igisubizo_cya_ai})
        
        # Rerun kugira ngo ifoto ishire mu kiganiro cyo hasi
        __streamlit__.rerun()
        
    except Exception as e:
        __streamlit__.error(f"Habaye ikibazo cyo gushaka igisubizo cyangwa processing y'ifoto: {e}")
