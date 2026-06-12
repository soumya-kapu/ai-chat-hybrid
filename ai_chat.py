import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Hybrid Router Pro", layout="wide")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ AI Controls")

api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

mode = st.sidebar.selectbox(
    "AI Mode",
    ["Smart Answer", "Simple Explanation", "Code Assistant"]
)

clear = st.sidebar.button("🧹 Clear Chat")

if clear:
    st.session_state.messages = []

st.title("🤖 AI Router Pro (Upgraded)")

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ----------------
user_input = st.chat_input("Ask something...")

# ---------------- SYSTEM PROMPT ----------------
def get_system_prompt(mode):
    if mode == "Smart Answer":
        return "You are a highly intelligent assistant that gives accurate and structured answers."
    elif mode == "Simple Explanation":
        return "Explain everything in very simple, beginner-friendly language."
    elif mode == "Code Assistant":
        return "You are a coding expert. Give clean, optimized code with explanation."
    return "You are a helpful assistant."

# ---------------- RESPONSE ----------------
if user_input and api_key:
    client = OpenAI(api_key=api_key)

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤖"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": get_system_prompt(mode)},
                    *[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]
                ]
            )

            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

elif user_input and not api_key:
    st.warning("Please enter OpenAI API key in sidebar")
