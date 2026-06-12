import streamlit as st
import requests
import openai
client = OpenAI()

st.set_page_config(page_title="Smart Hybrid AI Router", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Settings")

mode = st.sidebar.radio(
    "Choose Mode",
    ["Smart Auto", "Local AI (Ollama)", "Cloud AI (BYOK)"]
)

personality = st.sidebar.selectbox(
    "AI Personality",
    ["General Assistant", "Tutor", "Coder", "Research Analyst"]
)

api_key = None
client = None

if mode == "Cloud AI (BYOK)" or mode == "Smart Auto":
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    if api_key:
        client = OpenAI(api_key=api_key)

st.title("🧠 Smart Hybrid AI Router")

st.markdown("### ⚡ Local + 🌍 Cloud + 🧠 Smart AI System")

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- FUNCTIONS ----------------
def build_prompt(user_input):
    return f"""
You are a {personality}.
Respond accordingly.

User: {user_input}
"""

def local_ai(prompt):
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )
    return res.json()["response"]

def cloud_ai(prompt):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content

def smart_router(text):
    hard_words = ["explain", "analyze", "why", "compare", "design"]
    return "cloud" if any(w in text.lower() for w in hard_words) else "local"

# ---------------- INPUT ----------------
user_input = st.chat_input("Type your message...")

# ---------------- PROCESS ----------------
if user_input:

    prompt = build_prompt(user_input)

    if mode == "Local AI (Ollama)":
        answer = local_ai(prompt)

    elif mode == "Cloud AI (BYOK)":
        if not api_key:
            st.error("Please enter API key")
            st.stop()
        answer = cloud_ai(prompt)

    else:
        route = smart_router(user_input)
        if route == "cloud":
            if not api_key:
                st.error("Please enter API key")
                st.stop()
            answer = cloud_ai(prompt)
        else:
            answer = local_ai(prompt)

    st.session_state.history.append(("user", user_input))
    st.session_state.history.append(("ai", answer))

# ---------------- CHAT UI (NEW UPGRADE) ----------------
for role, msg in st.session_state.history:

    if role == "user":
        st.markdown(
            f"""
            <div style='text-align:right; background:#DCF8C6; padding:10px; border-radius:10px; margin:5px'>
                🧑 {msg}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='text-align:left; background:#F1F0F0; padding:10px; border-radius:10px; margin:5px'>
                🤖 {msg}
            </div>
            """,
            unsafe_allow_html=True
        )
