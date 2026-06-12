import streamlit as st

st.set_page_config(page_title="AI Hybrid Chat (BYOK + Ollama)", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ AI Settings")

mode = st.sidebar.selectbox(
    "Choose Mode",
    ["OpenAI (BYOK)", "Ollama (Local AI - Coming Soon)"]
)

api_key = None

if mode == "OpenAI (BYOK)":
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

st.title("🤖 AI Hybrid Chat App")

user_input = st.text_input("Ask your question")

# ---------------- OPENAI MODE ----------------
if mode == "OpenAI (BYOK)" and api_key and user_input:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    st.success(response.choices[0].message.content)

# ---------------- OLLAMA PLACEHOLDER ----------------
elif mode == "Ollama (Local AI - Coming Soon)":
    st.info("Ollama integration will be added here. Ensure Ollama is running locally.")

# ---------------- DEFAULT ----------------
elif user_input and not api_key:
    st.warning("Please enter API key in sidebar to use OpenAI mode.")
