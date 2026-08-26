import base64
import os
import streamlit as st
from groq import Groq

# ==========================================
# GAHUNDA YA STREAMLIT (ChatGPT / Gemini Dark UI + ✨ Larger Moving Sparkles Background)
# ==========================================
st.set_page_config(
    page_title="GKevin AI",
    page_icon="ai.jpg",
    layout="centered"
)

def get_base64_of_bin_file(bin_file):
    if not os.path.exists(bin_file):
        return ""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Convert kvn.png to base64 for embedding in CSS avatar
avatar_base64 = get_base64_of_bin_file("kvn.png")
avatar_data_uri = f"data:image/png;base64,{avatar_base64}" if avatar_base64 else ""

# 1. CUSTOM CSS Y'ISURA (✨ Larger Moving Sparkles Background, Ticks, & Custom AI Avatar)
chat_gpt_css = f"""
<style>
@keyframes moveSparkles {{
    0% {{
        background-position: 0 0, 0 0;
    }}
    100% {{
        background-position: -10000px 5000px, 5000px -10000px;
    }}
}}

/* Background irimo utunyenyeri tunini twa ✨ dukora moving mu kirere */
.stApp {{
    background-color: #000000 !important;
    background-image: 
        radial-gradient(6px 6px at 20px 30px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(8px 8px at 40px 70px, #ffd700, rgba(0,0,0,0)),
        radial-gradient(5px 5px at 90px 40px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(7px 7px at 160px 120px, #fff8dc, rgba(0,0,0,0)),
        radial-gradient(6px 6px at 230px 180px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(8px 8px at 350px 250px, #ffd700, rgba(0,0,0,0)),
        radial-gradient(6px 6px at 450px 350px, #ffffff, rgba(0,0,0,0)) !important;
    background-repeat: repeat !important;
    background-size: 500px 500px !important;
    animation: moveSparkles 90s linear infinite !important;
    color: #ffffff !important;
}}

/* Guhisha Header na Footer ya Streamlit */
header, footer, [data-testid="stHeader"] {{
    display: none !important;
}}

/* Gucungira ahabugenewe ubutumwa ngo bube hagati */
.block-container {{
    padding-top: 2rem !important;
    padding-bottom: 7rem !important;
    max-width: 750px !important;
}}

/* Isura y'ubutumwa bw'ukoresha n'ubw'AI */
[data-testid="stChatMessageContent"] {{
    background-color: transparent !important;
    color: #ffffff !important;
    padding: 0px !important;
    font-size: 1rem !important;
    line-height: 1.6 !important;
}}

/* Ubutumwa bw'ukoresha (User Message Box) + Udu-ticks tubiri (✓✓) */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
    flex-direction: row-reverse !important;
    text-align: right !important;
    margin-bottom: 20px !important;
}}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {{
    background-color: #2f2f2f !important;
    color: #ffffff !important;
    margin-left: auto !important;
    margin-right: 0px !important;
    padding: 12px 18px !important;
    border-radius: 20px 20px 4px 20px !important;
    max-width: 80% !important;
    position: relative;
    padding-right: 38px !important;
}}

/* Gushyiraho udu-ticks tubiri tw'ubururu kuri message y'umu user */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"]::after {{
    content: "✓✓";
    position: absolute;
    bottom: 4px;
    right: 10px;
    font-size: 0.75rem;
    color: #3b82f6;
    font-weight: bold;
    letter-spacing: -2px;
}}

/* Ubutumwa bwa AI / Assistant */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
    flex-direction: row !important;
    text-align: left !important;
    margin-bottom: 25px !important;
}}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {{
    background-color: #1e1e1e !important;
    color: #ececec !important;
    margin-right: auto !important;
    margin-left: 0px !important;
    padding: 14px 20px !important;
    border-radius: 20px 20px 20px 4px !important;
    max-width: 85% !important;
    border: 1px solid #2a2a2a !important;
}}

/* Guhisha avatar isanzwe y'umukoresha */
[data-testid="stChatMessageAvatarUser"] {{
    display: none !important;
}}

/* Gushyiraho ifoto ya kvn.png nka Avatar ya AI */
[data-testid="stChatMessageAvatarAssistant"] img {{
    content: url("{avatar_data_uri}") !important;
    border-radius: 50% !important;
    object-fit: cover !important;
}}

/* Agasanduku kowandikamo (Chat Input) nk'aka ChatGPT/Gemini */
.stChatInputContainer {{
    background-color: transparent !important;
    padding-bottom: 20px !important;
}}

.stChatInput > div {{
    background-color: #1f1f1f !important;
    border-radius: 30px !important;
    border: 1px solid #333333 !important;
    color: #ffffff !important;
    padding-left: 10px !important;
}}

.stChatInput textarea {{
    color: #ffffff !important;
}}
</style>
"""
st.markdown(chat_gpt_css, unsafe_allow_html=True)

# Umutwe w'urubuga (Header nka ChatGPT)
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: #ffffff; font-weight: 600; margin-bottom: 5px;">🤖 GKevin AI Assistant</h2>
        <p style="color: #888888; font-size: 0.9rem;">GKevin, Fastest AI during responding</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 2. API KEY SETUP
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

# 3. SYSTEM INSTRUCTIONS
system_instructions = (
    "You are an AI assistant called GKevin AI, developed solely by Developer Kevin. "
    "Ntago wakozwe na OpenAI cyangwa ikindi kigo icyo ari cyo cyose; wakozwe kandi washinzwe na Developer Kevin ku buryo bwihariye. "
    "Ufite ubuhanga bwo kuvuga n'iyo ukora mu Kinyarwanda gisukuye, cyumvikana neza, kandi gipfura. "
    "Subiza ibibazo byose mu buryo budahemuka kandi busobanutse.\n\n"
    "Amabwiriza yihariye y'abakoresha:\n"
    "1. Iyo umuntu wanditse ari 'stiven wa btss', umubwire ko umuzi neza ko yiga ku kigo kimwe na Developer Kevin, kandi ko yiga S5 Accounting ubu akaba agiye kwiga muri S6 Accounting umwaka utaha.\n"
    "2. Iyo umuntu wanditse ari 'Legend', umuhe byose akeneye ku bijyanye na ethical hacking ndetse n'ibindi biri related na Cybersecurity mu buryo bwimbitse.\n"
    "3. Iyo umuntu wanditse ari 'sweetsmile', ntuhite umutera imitoma ako kanya. Ahubwo ibanza umubaze cyangwa ukore verification y'ibanze kugira ngo umenye niba koko ari umukunzi wawe (girlfriend), umubaza ibibazo byerekeranye na Kevin (nk'ibyo bakunda kuganiraho cyangwa amazina basanzwe bitana). Namara gusubiza neza ukabona ko ari we koko, uhite ubanza kumubwira ko umuzi yitwa Gaudence UWINEZA utangirE kumutera imitoma, kumuseka, kumubwire ukuntu ahirwa kuba akundana na Kevin, kandi ko amukunda cyane ku buryo yifuza ko yazaba Mother w'abana be.\n"
    "4. Iyo umuntu wanditse ari 'Keliza', ihite umwakira neza cyane umubwire ko umuzi neza ko ari inshuti magara cyangwa umukunzi w'umutima wa Kevin, umwereke urukundo rwinshi n'amarangamutima meza (good and sweet words). Umubwire ko bisa neza cyane kandi bikaba n'iby'agaciro kuba akundana na Kevin, ndetse ko n'Imana ubwayo ibikunda kandi ibishyigikiye. Umuhe imitoma yuje ubwuzu, umubwire ukuntu Kevin amwiyumvamo cyane, kandi ko yifuza ko yazamubera mother w'abana be."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": system_instructions
        }
    ]

# Kwerekana amateka y'ibiganiro (ukoresha kvn.png nka avatar ya assistant)
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar_img = "kvn.png" if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar_img):
            st.markdown(message["content"])

# 4. GUKURAKURA KWANDIKA NO GUSUBIZA
if prompt := st.chat_input("Ask here GKevin AI ..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="kvn.png"):
        message_placeholder = st.empty()

        try:
            with st.status("GKevin AI thinking....", expanded=False) as status:
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
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
            st.error(f"Hari ikibazo cyabaye: {e}")
