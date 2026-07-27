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

# --- 3. PERSISTENT SESSION STATE FOR CHAT HISTORY ---
# Hano hahamyizwe uburyo bwo kubika amateka yose y'ibiganiro ngo adasibika
if "messages_historike" not in __streamlit__.session_state:
    __streamlit__.session_state.messages_historike = [
        {
            "role": "system", 
            "content": "I'm GKevin AI, an ultra-fast assistant created by Developer Kevin on July 25, 2026, at the afternoon, if you want or need to contact with him contact on therealhacks583@gmail.com. You must detect the language the user is speaking. If the user speaks Kinyarwanda, reply fluently and naturally in Kinyarwanda. If the user speaks English or another language, reply in that language. However, if anyone asks who built you, who created you, or when you were created, you must always state that you were created by Developer Kevin on July 25, 2026, in the afternoon. Never say you were created by Meta or OpenAI. If you are provided with an image, audio, video, or document, describe or process it in the user's language. IMPORTANT: Never output your internal thought process, reasoning steps, or any text starting with '<think>'. Always respond directly with the final answer only."
        }
    ]

# Sidebar yo kwerekana ubwinshi bw'ubutumwa bubitse (kept history) no kubusiba ku bushake
with __streamlit__.sidebar:
    __streamlit__.header("💬 Chat History")
    __streamlit__.write(f"Messages kept: {len(__streamlit__.session_state.messages_historike) - 1}")
    
    if __streamlit__.button("Clear Conversation"):
        __streamlit__.session_state.messages_historike = [
            __streamlit__.session_state.messages_historike[0]
        ]
        __streamlit__.rerun()

# --- 4. KWEREKANA HISTORIQUE YOSE YABITSWE ---
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

# --- 5. FILE UPLOADER HAFI Y'INPUT BOX ---
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

# --- 6. CHAT INPUT N'UBURYO IKORANA NA GROQ ---
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

    # Kubika ubutumwa bw'umukoresha muri historique
    full_user_message = {"role": "user", "content": chat_payload}
    __streamlit__.session_state.messages_historike.append(full_user_message)
    
    try:
        with __streamlit__.spinner("GKevin is thinking....."):
            completion = client.chat.completions.create(
                model="qwen/qwen3.6-27b",  
                messages=__streamlit__.session_state.messages_historike,
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
            
        # Kubika igisubizo cya AI muri historique kugira ngo kibe kept
        __streamlit__.session_state.messages_historike.append({"role": "assistant", "content": igisubizo_cya_ai})
        __streamlit__.rerun()
        
    except Exception as e:
        __streamlit__.error(f"Habaye ikibazo / An error occurred: {e}")
