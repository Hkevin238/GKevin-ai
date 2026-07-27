import streamlit as __streamlit__
from openai import OpenAI
import base64
from PIL import Image
import io
import pypdf

# --- 1. PAGE CONFIG ---
__streamlit__.set_page_config(
    page_title="GKevin AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --- CSS YA CHATGPT-LIKE HAMWE N'ANIMATION (FLOATING & SOFT RAINBOW BG) ---
st_css = """
<style>
    /* Uburyo background yihindura buhoro buhoro mu mabara y'umukororbya yoroshye */
    @keyframes softRainbowBg {
        0% { background-color: #1a1a2e; }
        25% { background-color: #1f1a24; }
        50% { background-color: #1a202c; }
        75% { background-color: #201a22; }
        100% { background-color: #1a1a2e; }
    }

    .stApp {
        animation: softRainbowBg 15s ease infinite;
    }

    /* Uburyo bwo kuzamura no kumanika ijambo ry'imitwe (Floating Animation) */
    @keyframes floatUpDown {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }

    .animated-title {
        animation: floatUpDown 2.5s ease-in-out infinite;
        display: inline-block;
        color: #ffffff;
    }

    /* Gukora ngo input box igororoke nkiya ChatGPT */
    div[data-testid="stChatInput"] {
        border-radius: 8px !important;
        border: 1px solid #ccc;
    }
    div[data-testid="stChatInputSubmitButton"] {
        border-radius: 0px !important;
    }
</style>
"""
__streamlit__.markdown(st_css, unsafe_allow_html=True)

# Gukoresha HTML na CSS kugira ngo Title igende izamuka imanuka idahagarara
__streamlit__.markdown(
    '<h1 class="animated-title">🤖 GKevin AI Assistant</h1>', 
    unsafe_allow_html=True
)
__streamlit__.write("This Assistant was built for You . WELCOME !")

# --- 2. HUZA NA GROQ API ---
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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"
)

# --- 3. DATABASE Y'ABAKORESHA (USER ACCOUNTS DATABASE) MURI SESSION STATE ---
if "users_db" not in __streamlit__.session_state:
    __streamlit__.session_state.users_db = {}  # {email: password}

if "logged_in_user" not in __streamlit__.session_state:
    __streamlit__.session_state.logged_in_user = None

if "user_histories" not in __streamlit__.session_state:
    __streamlit__.session_state.user_histories = {}  # {email: messages_list}


# --- 4. AUTHENTICATION (LOGIN & SIGN UP SIDEBAR) ---
with __streamlit__.sidebar:
    __streamlit__.header("🔐 Account Authentication")
    
    if __streamlit__.session_state.logged_in_user is None:
        auth_mode = __streamlit__.radio("Hitamo uburyo:", ["Login (Injira)", "Sign Up (Iyandikishe)"])
        
        email_input = __streamlit__.text_input("Email Address")
        password_input = __streamlit__.text_input("Password", type="password")
        
        if auth_mode == "Sign Up (Iyandikishe)":
            if __streamlit__.button("Create Account"):
                if not email_input or not password_input:
                    __streamlit__.error("Uzuza email na password neza!")
                elif email_input in __streamlit__.session_state.users_db:
                    __streamlit__.warning("Iyi email isanzwe ikoreshwa! Injira cyangwa ukoreshe indi.")
                else:
                    __streamlit__.session_state.users_db[email_input] = password_input
                    __streamlit__.session_state.user_histories[email_input] = [
                        {
                            "role": "system", 
                            "content": "I'm GKevin AI, an ultra-fast assistant created by Developer Kevin on July 25, 2026, at the afternoon, if you want or need to contact with him contact on therealhacks583@gmail.com. You must detect the language the user is speaking. If the user speaks Kinyarwanda, reply fluently and naturally in Kinyarwanda. If the user speaks English or another language, reply in that language. However, if anyone asks who built you, who created you, or when you were created, you must always state that you were created by Developer Kevin on July 25, 2026, in the afternoon. Never say you were created by Meta or OpenAI. If you are provided with an image, audio, video, or document, describe or process it in the user's language. IMPORTANT: Never output your internal thought process, reasoning steps, or any text starting with '<think>'. Always respond directly with the final answer only."
                        }
                    ]
                    __streamlit__.success("Account Created Successfully! You can (Login).")
        
        else:  # Login Mode
            if __streamlit__.button("Login"):
                if email_input in __streamlit__.session_state.users_db and __streamlit__.session_state.users_db[email_input] == password_input:
                    __streamlit__.session_state.logged_in_user = email_input
                    __streamlit__.success(f"Your Welcome !, {email_input}!")
                    __streamlit__.rerun()
                else:
                    __streamlit__.error("Email or password is incorrect!")
                    
        __streamlit__.info("Please Sign in into your account in order to access GKevin AI Assistant.")
        __streamlit__.stop()

    else:
        # Niba umukoresha yamaze kwinjira (Logged In)
        __streamlit__.success(f"Logged in as: {__streamlit__.session_state.logged_in_user}")
        
        __streamlit__.header("💬 Chat History")
        current_user = __streamlit__.session_state.logged_in_user
        msg_count = len(__streamlit__.session_state.user_histories.get(current_user, [])) - 1
        __streamlit__.write(f"Messages kept: {max(0, msg_count)}")
        
        if __streamlit__.button("Clear Conversation"):
            system_msg = __streamlit__.session_state.user_histories[current_user][0]
            __streamlit__.session_state.user_histories[current_user] = [system_msg]
            __streamlit__.rerun()
            
        if __streamlit__.button("Log Out (Sohoka)"):
            __streamlit__.session_state.logged_in_user = None
            __streamlit__.rerun()


# --- 5. KWEREKANA HISTORIQUE Y'UMUKORESHAGIYE WEMEJWE ---
active_user = __streamlit__.session_state.logged_in_user
if active_user not in __streamlit__.session_state.user_histories:
    __streamlit__.session_state.user_histories[active_user] = [
        {
            "role": "system", 
            "content": "I'm GKevin AI, an ultra-fast assistant created by Developer Kevin on July 25, 2026, at the afternoon, if you want or need to contact with him contact on therealhacks583@gmail.com. You must detect the language the user is speaking. If the user speaks Kinyarwanda, reply fluently and naturally in Kinyarwanda. If the user speaks English or another language, reply in that language. However, if anyone asks who built you, who created you, or when you were created, you must always state that you were created by Developer Kevin on July 25, 2026, in the afternoon. Never say you were created by Meta or OpenAI. If you are provided with an image, audio, video, or document, describe or process it in the user's language. IMPORTANT: Never output your internal thought process, reasoning steps, or any text starting with '<think>'. Always respond directly with the final answer only."
        }
    ]

user_messages_list = __streamlit__.session_state.user_histories[active_user]

for message in user_messages_list:
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

# --- 6. FILE UPLOADER HAFI Y'INPUT BOX ---
col_file, col_empty = __streamlit__.columns([3, 7])
with col_file:
    uploaded_file = __streamlit__.file_uploader(
        "➕ Attach File", 
        type=["png", "jpg", "jpeg", "pdf", "txt", "csv", "docx", "mp3", "wav", "mp4", "mov"],
        label_visibility="collapsed"
    )

if uploaded_file is not None:
    if uploaded_file.type.startswith("image/"):
        __streamlit__.caption(f"🖼️ Image attached: {uploaded_file.name}")
    elif uploaded_file.type.startswith("audio/"):
        __streamlit__.caption(f"🎵 Audio attached: {uploaded_file.name}")
    elif uploaded_file.type.startswith("video/"):
        __streamlit__.caption(f"🎬 Video attached: {uploaded_file.name}")
    else:
        __streamlit__.caption(f"📎 File attached: {uploaded_file.name}")

# --- 7. CHAT INPUT N'UBURYO IKORANA NA GROQ ---
if ikibazo := __streamlit__.chat_input("Type here...."):
    
    chat_payload = []
    file_text_content = ""
    
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            try:
                reader = pypdf.PdfReader(uploaded_file)
                for page in reader.pages:
                    file_text_content += page.extract_text() + "\n"
            except Exception as e:
                file_text_content = f"[Error reading PDF: {e}]"
        elif uploaded_file.type == "text/plain":
            file_text_content = uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.type.startswith("audio/"):
            file_text_content = f"[Attached Audio File: {uploaded_file.name}]"
        elif uploaded_file.type.startswith("video/"):
            file_text_content = f"[Attached Video File: {uploaded_file.name}]"
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/csv"]:
            file_text_content = f"[Attached Document: {uploaded_file.name}]"

    full_query = ikibazo
    if file_text_content and not uploaded_file.type.startswith("image/"):
        full_query = f"{ikibazo}\n\nHere is information about the attached file ({uploaded_file.name}):\n{file_text_content}"

    if full_query:
        __streamlit__.chat_message("user").markdown(ikibazo)
        if uploaded_file is not None:
            if uploaded_file.type.startswith("audio/"):
                __streamlit__.audio(uploaded_file)
            elif uploaded_file.type.startswith("video/"):
                __streamlit__.video(uploaded_file)
                
        chat_payload.append({"type": "text", "text": full_query})

    if uploaded_file is not None and uploaded_file.type.startswith("image/"):
        with __streamlit__.chat_message("user"):
            __streamlit__.image(uploaded_file)
            
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        mime_type = uploaded_file.type
        
        chat_payload.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
        })

    # Kubika ubutumwa bw'umukoresha muri historique ye bwite
    full_user_message = {"role": "user", "content": chat_payload}
    __streamlit__.session_state.user_histories[active_user].append(full_user_message)
    
    try:
        with __streamlit__.spinner("GKevin is thinking....."):
            completion = client.chat.completions.create(
                model="qwen/qwen3.6-27b",  
                messages=__streamlit__.session_state.user_histories[active_user],
                temperature=0.7,
                max_tokens=1024
            )
            
            igisubizo_cya_ai = completion.choices[0].message.content
            
            # Gukumira burundu <think> tag
            if "<think>" in igisubizo_cya_ai:
                parts = igisubizo_cya_ai.split("</think>")
                if len(parts) > 1:
                    igisubizo_cya_ai = parts[-1].strip()
            
            igisubizo_cya_ai = igisubizo_cya_ai.replace("<think>", "").replace("</think>", "").strip()
            
        # Kubika igisubizo cya AI muri historique y'uwo mukoresha
        __streamlit__.session_state.user_histories[active_user].append({"role": "assistant", "content": igisubizo_cya_ai})
        __streamlit__.rerun()
        
    except Exception as e:
        __streamlit__.error(f"Habaye ikibazo / An error occurred: {e}")
