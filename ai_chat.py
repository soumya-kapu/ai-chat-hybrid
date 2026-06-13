import streamlit as st
import PyPDF2

st.set_page_config(
    page_title="Smart PDF & Career Assistant",
    layout="wide"
)

st.title("📄 Smart PDF & Career Assistant")

st.sidebar.title("⚙️ Features")

feature = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Smart PDF Simplifier",
        "Resume Matcher"
    ]
)

# =========================
# SMART PDF SIMPLIFIER
# =========================

if feature == "Smart PDF Simplifier":

    st.subheader("📄 Smart PDF Simplifier")

    uploaded_file = st.file_uploader(
        "Upload a PDF File",
        type=["pdf"]
    )

    if uploaded_file:

        reader = PyPDF2.PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        words = text.split()

        st.success("✅ PDF Processed Successfully")

        # Document Statistics
        st.write("## 📊 Document Statistics")

        pages = len(reader.pages)
        word_count = len(words)
        reading_time = max(1, round(word_count / 200))

        col1, col2, col3 = st.columns(3)

        col1.metric("Pages", pages)
        col2.metric("Words", word_count)
        col3.metric("Reading Time", f"{reading_time} min")

        # Summary
        st.write("## 📝 Short Summary")

        summary = " ".join(words[:200])

        st.info(summary + "...")

        # Key Points
        st.write("## 🔑 Key Points")

        sentences = text.split(".")

        shown = 0

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence) > 40:
                st.write(f"• {sentence}")
                shown += 1

            if shown == 5:
                break

        # Keywords
        st.write("## 🎯 Important Keywords")

        keywords = []

        for word in words:

            clean_word = word.lower().strip(
                ",.!?;:()[]{}"
            )

            if (
                len(clean_word) > 5
                and clean_word not in keywords
            ):
                keywords.append(clean_word)

        st.success(", ".join(keywords[:20]))

        # Study Questions
        st.write("## ❓ Study Questions")

        st.write("1. What is the main topic of this document?")
        st.write("2. Which concepts are most important?")
        st.write("3. What conclusions are presented?")
        st.write("4. What should a student remember?")
        st.write("5. Which areas need further study?")

# =========================
# RESUME MATCHER
# =========================

elif feature == "Resume Matcher":

    st.subheader("💼 Resume vs Job Match Tool")

    resume = st.text_area("Paste Resume")

    job = st.text_area("Paste Job Description")

    if resume and job:

        resume_words = set(resume.lower().split())
        job_words = set(job.lower().split())

        match_score = (
            len(resume_words & job_words)
            / len(job_words)
        ) * 100

        st.metric(
            "Match Score",
            f"{match_score:.2f}%"
        )

        if match_score > 60:
            st.success("🎯 Good Match")
        elif match_score > 30:
            st.warning("⚠️ Partial Match")
        else:
            st.error("❌ Low Match")
