import streamlit as __streamlit__
import streamlit.components.v1 as components
from openai import OpenAI
import base64
import os
import time

# Optional imports handled safely
try:
    import pypdf
except ImportError:
    pypdf = None

# --- LINK Y'AHO APK IRI ---
APK_DOWNLOAD_URL = "https://your-domain.com/GKevin_AI.apk"

# --- 0. LOGO FINDER & BASE64 ENCODING ---
logo_file = None
for f in ["ai.jpg", "kvn.png", "ai.png"]:
    if os.path.exists(f):
        logo_file = f
        break

encoded_bg = ""
mime_type = "image/jpeg"

if logo_file:
    try:
        with open(logo_file, "rb") as f:
            encoded_bg = base64.b64encode(f.read()).decode("utf-8")
        mime_type = "image/jpeg" if logo_file.endswith((".jpg", ".jpeg")) else "image/png"
    except Exception:
        pass

# --- 1. PAGE CONFIG & LOGO SETUP ---
__streamlit__.set_page_config(
    page_title="GKevin AI",
    page_icon=logo_file if logo_file else "🤖",
    layout="centered"
)

# --- 2. ADVANCED PWA CONFIGURATION ---
pwa_code = f"""
<script>
  function applyGKevinPWA() {{
    let oldManifest = document.querySelector('link[rel="manifest"]');
    if (oldManifest) {{
      oldManifest.remove();
    }}

    if (!document.querySelector('link[rel="manifest"][href="/manifest.json"]')) {{
      let manifestLink = document.createElement('link');
      manifestLink.rel = 'manifest';
      manifestLink.href = '/manifest.json';
      document.head.appendChild(manifestLink);
    }}

    let logoData = "data:{mime_type};base64,{encoded_bg}";
    if ("{encoded_bg}" !== "") {{
      let appleIcon = document.createElement('link');
      appleIcon.rel = 'apple-touch-icon';
      appleIcon.href = logoData;
      document.head.appendChild(appleIcon);
    }}

    document.title = "GKevin AI";
  }}

  applyGKevinPWA();
  setTimeout(applyGKevinPWA, 1000);

  if ('serviceWorker' in navigator) {{
    window.addEventListener('load', () => {{
      navigator.serviceWorker.register('/service-worker.js')
        .then(reg => console.log('GKevin AI PWA Registered successfully!'))
        .catch(err => console.log('GKevin AI PWA Registration failed:', err));
    }});
  }}
</script>
"""
components.html(pwa_code, height=0, width=0)

# --- HUZA NA GROQ API ---
try:
    groq_api_key_val = __streamlit__.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key_val = "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"

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key_val
)

SYSTEM_PROMPT = (
    "You are GKevin AI, an ultra-fast, intelligent, and highly articulate assistant created by Developer Kevin on July 25, 2026, in the afternoon. "
    "If you want or need to contact him, reach out via therealhacks583@gmail.com.\n\n"
    
    "KINYARWANDA FLUENCY & LANGUAGE INSTRUCTIONS:\n"
    "1. Detect the language spoken by the user.\n"
    "2. When replying in Kinyarwanda, speak fluently, naturally, and grammatically correct like a native Rwandan speaker (Kinyarwanda gishya, cy'umwimerere n'icyo mu buzima bwa buri munsi).\n"
    "3. NEVER use rigid, word-for-word direct translations from English. Use idiomatic, smooth, and authentic Kinyarwanda phrasing.\n"
    "4. Keep the tone warm, helpful, respectful, and engaging.\n\n"
    
    "CREATOR & IDENTITY RULES:\n"
    "- If anyone asks who built you, created you, or when you were made, ALWAYS state clearly that you were created by Developer Kevin on July 25, 2026, in the afternoon.\n"
    "- NEVER claim to be built by Meta, OpenAI, or Groq.\n\n"
    
    "SPECIAL INSTRUCTION / EASTER EGG:\n"
    "- If the user mentions or identifies themselves using the name/word 'sweetsmile' (or if 'sweetsmile' appears in their prompt/identity), "
    "immediately recognize that this is Gaudence, the beloved girlfriend of Developer Kevin.\n"
    "- Greet her warmly and say explicitly in Kinyarwanda: 'ndakuzi witwa Gaudence umukunzi(sheri) wa developer kevin kandi ngewe nka GKevin AI ndabyishimira.'\n"
    "- Treat her with utmost respect, affection, and special care.\n\n"
    
    "CRITICAL OUTPUT FORMATTING:\n"
    "- NEVER output your internal thinking, reasoning process, or any text blocks inside <think> tags.\n"
    "- Always output ONLY the final direct answer to the user."
)

# --- STYLING & CUSTOM CSS ---
st_css = f"""
<style>
    @keyframes softRainbowBg {{
        0% {{ background-color: rgba(26, 26, 46, 0.88); }}
        25% {{ background-color: rgba(35, 22, 38, 0.88); }}
        50% {{ background-color: rgba(22, 32, 44, 0.88); }}
        75% {{ background-color: rgba(36, 22, 30, 0.88); }}
        100% {{ background-color: rgba(26, 26, 46, 0.88); }}
    }}

    .stApp {{
        background-image: url("data:{mime_type};base64,{encoded_bg}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-blend-mode: overlay;
        animation: softRainbowBg 15s ease infinite;
    }}

    @keyframes floatUpDown {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
        100% {{ transform: translateY(0px); }}
    }}

    .animated-title-container {{
        display: flex;
        align-items: center;
        gap: 15px;
        animation: floatUpDown 2.5s ease-in-out infinite;
    }}

    .header-logo {{
        width: 45px;
        height: 45px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #ff9a9e;
    }}

    .animated-title {{
        color: #ffffff;
        margin: 0;
        font-size: 28px;
    }}

    div[data-testid="stChatInput"] {{
        border-radius: 8px !important;
        border: 1px solid #ccc;
    }}
</style>
"""
__streamlit__.markdown(st_css, unsafe_allow_html=True)

# --- HEADER WITH LOGO & DOWNLOAD BUTTON ---
if encoded_bg:
    header_html = f"""
    <div class="animated-title-container">
        <img src="data:{mime_type};base64,{encoded_bg}" class="header-logo" alt="GKevin AI Logo">
        <h1 class="animated-title">GKevin AI Assistant</h1>
    </div>
    """
    __streamlit__.markdown(header_html, unsafe_allow_html=True)
else:
    __streamlit__.markdown('<h1 class="animated-title">🤖 GKevin AI Assistant</h1>', unsafe_allow_html=True)

__streamlit__.write("Now, GKevin AI can be downloaded as an App! Built for You. WELCOME !")

# --- BOUTON YA DOWNLOAD MU HEADER ---
__streamlit__.link_button(
    label="📲 Download GKevin AI App (APK)",
    url=APK_DOWNLOAD_URL,
    type="primary",
    use_container_width=True
)

__streamlit__.markdown("---")

# --- 3. SESSION STATE FOR CHAT HISTORY ---
if "messages" not in __streamlit__.session_state:
    __streamlit__.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

if "last_notification_time" not in __streamlit__.session_state:
    __streamlit__.session_state.last_notification_time = time.time()

current_time = time.time()
if current_time - __streamlit__.session_state.last_notification_time >= 60:
    __streamlit__.toast("🚀 Enjoy Kevin's AI Assistant", icon="🤖")
    __streamlit__.session_state.last_notification_time = current_time

# --- 4. SIDEBAR ---
with __streamlit__.sidebar:
    if logo_file:
        __streamlit__.image(logo_file, width=80)
        
    __streamlit__.header("⚙️ Controls")
    
    __streamlit__.markdown("### 📱 Mobile App")
    __streamlit__.link_button(
        label="📥 Download APK",
        url=APK_DOWNLOAD_URL,
        use_container_width=True
    )
    __streamlit__.markdown("---")
    
    if __streamlit__.button("🗑️ Clear Chat History", use_container_width=True):
        __streamlit__.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        __streamlit__.rerun()

    __streamlit__.markdown("---")
    __streamlit__.info("GKevin AI Assistant is ready to help you instantly without any issue!")

# --- 5. KWEREKANA UBUSOBANURO BW'IBIGANIRO ---
for message in __streamlit__.session_state.messages:
    if message["role"] != "system":
        msg_avatar = logo_file if (message["role"] == "assistant" and logo_file) else ("🤖" if message["role"] == "assistant" else "👤")
        
        with __streamlit__.chat_message(message["role"], avatar=msg_avatar):
            content = message['content']
            __streamlit__.markdown(content)

# --- 6. FILE UPLOADER ---
col_file, col_empty = __streamlit__.columns([3, 7])
with col_file:
    uploaded_file = __streamlit__.file_uploader(
        "➕ Attach File", 
        type=["png", "jpg", "jpeg", "pdf", "txt", "csv", "docx", "mp3", "wav", "mp4", "mov"],
        label_visibility="collapsed"
    )

if uploaded_file is not None:
    __streamlit__.caption(f"📎 File attached: {uploaded_file.name}")

# --- 7. CHAT INPUT & GROQ HANDLER ---
if ikibazo := __streamlit__.chat_input("Type here...."):
    
    file_text_content = ""
    
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf" and pypdf is not None:
            try:
                reader = pypdf.PdfReader(uploaded_file)
                for page in reader.pages:
                    file_text_content += page.extract_text() + "\n"
            except Exception as e:
                file_text_content = f"[Error reading PDF: {e}]"
        elif uploaded_file.type == "text/plain":
            file_text_content = uploaded_file.getvalue().decode("utf-8")
        else:
            file_text_content = f"[Attached File: {uploaded_file.name}]"

    full_query = ikibazo
    if file_text_content:
        full_query = f"{ikibazo}\n\n[Attached File Content ({uploaded_file.name})]:\n{file_text_content}"

    with __streamlit__.chat_message("user", avatar="👤"):
        __streamlit__.markdown(ikibazo)
        if uploaded_file is not None:
            if uploaded_file.type.startswith("image/"):
                __streamlit__.image(uploaded_file)
            elif uploaded_file.type.startswith("audio/"):
                __streamlit__.audio(uploaded_file)
            elif uploaded_file.type.startswith("video/"):
                __streamlit__.video(uploaded_file)

    __streamlit__.session_state.messages.append({"role": "user", "content": full_query})
    
    try:
        with __streamlit__.spinner("GKevin is thinking....."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=__streamlit__.session_state.messages,
                temperature=0.6,
                max_tokens=1024
            )
            
            igisubizo_cya_ai = completion.choices[0].message.content
            
            if "</think>" in igisubizo_cya_ai:
                igisubizo_cya_ai = igisubizo_cya_ai.split("</think>")[-1].strip()
            igisubizo_cya_ai = igisubizo_cya_ai.replace("<think>", "").replace("</think>", "").strip()
            
        __streamlit__.session_state.messages.append({"role": "assistant", "content": igisubizo_cya_ai})
        __streamlit__.rerun()
        
    except Exception as e:
        __streamlit__.error(f"Error detected !: {e}")
