import streamlit as __streamlit__
from openai import OpenAI
import base64
from PIL import Image

# --- Gushyira ho CSS ya ChatGPT-like input box hamwe no guhindura Avatars ---
st_css = """
<style>
    /* Gukora ngo input box igororoke (square edges) nkiya ChatGPT */
    div[data-testid="stChatInput"] {
        border-radius: 8px !important;
        border: 1px solid #ccc;
    }
    /* Gukuraho 'rounded corners' kuri button yayo */
    div[data-testid="stChatInputSubmitButton"] {
        border-radius: 0px !important;
    }
    
    /* Guhindura Avatar ya Assistant (Gukoresha ai.jpg) */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarAssistant"]) img {
        content: url("ai.jpg");
        border-radius: 50%;
    }
    
    /* Guhindura Avatar y'Umukoresha (User) */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarUser"]) img {
        content: url("ai.jpg");
        border-radius: 50%;
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
            "content": "I'm GKevin AI, an ultra-fast assistant created by Developer Kevin on July 25, 2026, at the afternoon, if you want or need to contact with him contact on therealhacks583@gmail.com. You must detect the language the user is speaking. If the user speaks Kinyarwanda, reply fluently and naturally in Kinyarwanda. If the user speaks English or another language, reply in that language. However, if anyone asks who built you, who created you, or when you were created, you must always state that you were created by Developer Kevin on July 25, 2026, in the afternoon. Never say you were created by Meta or OpenAI. If you are provided with an image, describe or analyze what is in the image in the language the user is currently using. IMPORTANT: Never output your internal thought process, reasoning steps, or any text starting with '<think>'. Always respond directly with the final answer only."
        }
    ]

# 4. Sidebar History
with __streamlit__.sidebar:
    __streamlit__.header("💬 Chat History")
    
    if __streamlit__.button("Clear Conversation"):
        __streamlit__.session_state.messages_historike = [
            __streamlit__.session_state.messages_historike[0]
        ]
        __streamlit__.rerun()

    __streamlit__.markdown("---")
    
    # File Uploader muri Sidebar
    __streamlit__.subheader("🖼️ Attach an Image (Optional)")
    uploaded_file = __streamlit__.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    
    # Kwerekana ifoto yashyizemo muri sidebar
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        __streamlit__.image(image, caption="Uploaded Image", use_column_width=True)

# 5. Kwerekana ubutumwa bwose bwari busanzwe muri historique
for message in __streamlit__.session_state.messages_historike:
    if message["role"] != "system":
        with __streamlit__.chat_message(message["role"]):
            content = message['content']
            if isinstance(content, list):
                for item in content:
                    if item.get('type') == 'text':
                        __streamlit__.markdown(item['text'])
                    elif item.get('type') == 'image_url':
                        __streamlit__.image(item['image_url']['url'])
            else:
                __streamlit__.markdown(content)

# 6. Gufata ubutumwa bw'umukoresha
if ikibazo := __streamlit__.chat_input("Andika ubutumwa hano... / Type a message..."):
    
    chat_payload = []
    
    # Ongeramo text niba ihari
    if ikibazo:
        __streamlit__.chat_message("user").markdown(ikibazo)
        chat_payload.append({"type": "text", "text": ikibazo})

    # Hindura ifoto muri Base64 niba ihari
    if uploaded_file is not None:
        with __streamlit__.chat_message("user"):
            __streamlit__.image(uploaded_file)
            
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        mime_type = uploaded_file.type
        
        chat_payload.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
        })

    # Kongera ubutumwa muri historique
    full_user_message = {"role": "user", "content": chat_payload}
    __streamlit__.session_state.messages_historike.append(full_user_message)
    
    # Gusaba igisubizo muri Groq AI hamwe na Spinner ya pending ("GKevin is thinking.....")
    try:
        with __streamlit__.spinner("GKevin is thinking....."):
            completion = client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=__streamlit__.session_state.messages_historike,
                temperature=0.7,
                max_tokens=1024
            )
            
            igisubizo_cya_ai = completion.choices[0].message.content
            
            # Gukuraho burundu agace ka <think> niba kaje mu buryo bw'impanuka
            if "<think>" in igisubizo_cya_ai:
                parts = igisubizo_cya_ai.split("</think>")
                if len(parts) > 1:
                    igisubizo_cya_ai = parts[-1].strip()

        # Kwongera igisubizo cyiza cya AI muri historique
        __streamlit__.session_state.messages_historike.append({"role": "assistant", "content": igisubizo_cya_ai})
        
        # Rerun kugira ngo ibisubizo byose byerekanwe neza
        __streamlit__.rerun()
        
    except Exception as e:
        __streamlit__.error(f"Habaye ikibazo / An error occurred: {e}")
