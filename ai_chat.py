import streamlit as st
import PyPDF2

st.set_page_config(
    page_title="Smart PDF & Career Assistant",
    layout="wide"
)

translations = {
    "English": {
        "title": "📄 Smart PDF & Career Assistant",
        "pdf": "Smart PDF Simplifier",
        "resume": "Resume Matcher",
        "upload": "Upload a PDF File",
        "resume_text": "Paste Resume",
        "job_text": "Paste Job Description",
        "processed": "✅ PDF Processed Successfully"
    },
    "తెలుగు": {
        "title": "📄 స్మార్ట్ PDF & కెరీర్ అసిస్టెంట్",
        "pdf": "స్మార్ట్ PDF సరళీకరణ",
        "resume": "రెజ్యూమ్ మ్యాచ్",
        "upload": "PDF ఫైల్ అప్లోడ్ చేయండి",
        "resume_text": "రెజ్యూమ్ పేస్ట్ చేయండి",
        "job_text": "జాబ్ వివరణ పేస్ట్ చేయండి",
        "processed": "✅ PDF విజయవంతంగా ప్రాసెస్ చేయబడింది"
    },
    "हिन्दी": {
        "title": "📄 स्मार्ट PDF और करियर असिस्टेंट",
        "pdf": "स्मार्ट PDF सरलकर्ता",
        "resume": "रिज्यूमे मैचर",
        "upload": "PDF फ़ाइल अपलोड करें",
        "resume_text": "रिज्यूमे पेस्ट करें",
        "job_text": "जॉब विवरण पेस्ट करें",
        "processed": "✅ PDF सफलतापूर्वक प्रोसेस हो गई"
    }
}

language = st.sidebar.selectbox(
    "🌐 Language",
    ["English", "తెలుగు", "हिन्दी"]
)

t = translations[language]

st.title(t["title"])

feature = st.sidebar.selectbox(
    "Choose Feature",
    [t["pdf"], t["resume"]]
)

if feature == t["pdf"]:

    st.subheader("📄 " + t["pdf"])

    uploaded_file = st.file_uploader(
        t["upload"],
        type=["pdf"]
    )

    if uploaded_file:

        reader = PyPDF2.PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        words = text.split()

        st.success(t["processed"])

        st.write("## 📊 Document Statistics")

        pages = len(reader.pages)
        word_count = len(words)
        reading_time = max(1, round(word_count / 200))

        col1, col2, col3 = st.columns(3)

        col1.metric("Pages", pages)
        col2.metric("Words", word_count)
        col3.metric("Reading Time", f"{reading_time} min")

        st.write("## 📝 Short Summary")

        summary = " ".join(words[:200])

        st.info(summary + "...")

        st.write("## 🎯 Important Keywords")

        keywords = []

        for word in words:
            clean_word = word.lower().strip(",.!?;:()[]{}")

            if len(clean_word) > 5 and clean_word not in keywords:
                keywords.append(clean_word)

        st.success(", ".join(keywords[:20]))

elif feature == t["resume"]:

    st.subheader("💼 " + t["resume"])

    resume = st.text_area(t["resume_text"])

    job = st.text_area(t["job_text"])

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
