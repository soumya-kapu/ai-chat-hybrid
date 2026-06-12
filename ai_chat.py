import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Router Pro", layout="wide")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ AI Controls")

mode = st.sidebar.selectbox(
    "AI Mode",
    ["Smart Answer", "Simple Explanation", "Code Assistant"]
)

api_key = st.sidebar.text_input("Enter OpenAI API Key (only needed for AI replies)", type="password")

clear = st.sidebar.button("🧹 Clear Chat")

if clear:
    st.session_state.messages = []

st.title("🤖 AI Router Pro")

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ----------------
user_input = st.chat_input("Say something...")

# ---------------- SYSTEM PROMPT ----------------
def get_system_prompt(mode):
    if mode == "Smart Answer":
        return "You are a highly intelligent assistant."
    elif mode == "Simple Explanation":
        return "Explain in very simple language."
    elif mode == "Code Assistant":
        return "You are a coding expert."
    return "You are helpful."

# ---------------- LOGIC ----------------
if user_input:
    
    # show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    # CASE 1: NO API KEY → fallback response (NO ERROR)
    if not api_key:
        reply = "⚠️ Please enter API key to get AI response."

    # CASE 2: WITH API KEY → real OpenAI response
    else:
        client = OpenAI(api_key=api_key)

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
