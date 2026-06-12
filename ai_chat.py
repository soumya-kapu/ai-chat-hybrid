import streamlit as st
import PyPDF2

st.set_page_config(page_title="AI Study & Career Assistant", layout="wide")

# ---------------- SESSION ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Features")

feature = st.sidebar.selectbox(
    "Choose Feature",
    ["AI Chat (Demo)", "PDF Simplifier", "Resume Matcher"]
)

st.title("🤖 AI Study & Career Assistant")

# ---------------- AI CHAT (SAFE DEMO) ----------------
if feature == "AI Chat (Demo)":

    user_input = st.text_input("Ask anything")

    # show history
    for role, msg in st.session_state.chat:
        if role == "user":
            with st.chat_message("user"):
                st.markdown(msg)
        else:
            with st.chat_message("assistant"):
                st.markdown(msg)

    def demo_ai(text):
        text = text.lower()

        if "hello" in text:
            return "👋 Hello! I am your AI Study Assistant."

        elif "what is ai" in text or "ai" in text:
            return "🧠 AI is Artificial Intelligence."

        elif "pdf" in text:
            return "📄 Use PDF Simplifier for documents."

        elif "resume" in text:
            return "💼 Use Resume Matcher for job matching."

        else:
            return f"🤖 You said: {text}"

    if user_input:

        st.session_state.chat.append(("user", user_input))

        with st.chat_message("user"):
            st.markdown(user_input)

        reply = demo_ai(user_input)

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.chat.append(("bot", reply))
    for role, msg in st.session_state.chat:
        if role == "user":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 AI:** {msg}")

# ---------------- PDF SIMPLIFIER ----------------
elif feature == "PDF Simplifier":
    st.subheader("📄 Upload PDF to Simplify")

    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        st.write("### 📌 Simplified Summary")
        st.success(text[:2000] + " ...")

        st.info("✨ This is simplified extraction (you can enhance later with AI)")

# ---------------- RESUME MATCHER ----------------
elif feature == "Resume Matcher":
    st.subheader("🧠 Resume vs Job Match Tool")

    resume = st.text_area("Paste Resume")
    job = st.text_area("Paste Job Description")

    if resume and job:
        resume_words = set(resume.lower().split())
        job_words = set(job.lower().split())

        match_score = len(resume_words & job_words) / len(job_words) * 100

        st.metric("Match Score", f"{match_score:.2f}%")

        if match_score > 60:
            st.success("🎯 Good Match")
        elif match_score > 30:
            st.warning("⚠️ Partial Match")
        else:
            st.error("❌ Low Match")
