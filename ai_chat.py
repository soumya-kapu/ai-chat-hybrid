import streamlit as st
import PyPDF2
from deep_translator import GoogleTranslator

st.set_page_config(
    page_title="Smart PDF & Career Assistant",
    layout="wide"
)

translations = {
    "English": {
        "title": "📄 Smart PDF & Career Assistant",
        "pdf": "Smart PDF Simplifier",
        "resume": "Resume Matcher",
        "upload": "Upload a PDF File"
    },
    "తెలుగు": {
        "title": "📄 స్మార్ట్ PDF & కెరీర్ అసిస్టెంట్",
        "pdf": "స్మార్ట్ PDF సరళీకరణ",
        "resume": "రెజ్యూమ్ మ్యాచ్",
        "upload": "PDF ఫైల్ అప్లోడ్ చేయండి"
    },
    "हिन्दी": {
        "title": "📄 स्मार्ट PDF और करियर असिस्टेंट",
        "pdf": "स्मार्ट PDF सरलकर्ता",
        "resume": "रिज्यूमे मैचर",
        "upload": "PDF फ़ाइल अपलोड करें"
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
    [
        t["pdf"],
        t["resume"]
    ]
)


# -------------------------
# PDF SIMPLIFIER
# -------------------------

if feature == t["pdf"]:

    st.subheader(t["pdf"])

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


        if len(words) == 0:
            st.error(
                "No readable text found. This PDF may be scanned."
            )

        else:

            st.success(
                "✅ PDF Processed Successfully"
            )


            # Statistics

            st.write("## 📊 Document Statistics")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Pages",
                len(reader.pages)
            )

            col2.metric(
                "Words",
                len(words)
            )

            col3.metric(
                "Reading Time",
                f"{max(1, round(len(words)/200))} min"
            )


            # Summary

            st.write("## 📝 Smart Summary")


            summary = " ".join(words[:200])


            if language == "తెలుగు":

                summary = GoogleTranslator(
                    source="auto",
                    target="te"
                ).translate(summary)


            elif language == "हिन्दी":

                summary = GoogleTranslator(
                    source="auto",
                    target="hi"
                ).translate(summary)


            st.info(summary)


            # Keywords

            st.write("## 🎯 Important Keywords")


            keywords = []

            for word in words:

                clean = word.lower().strip(
                    ",.!?;:()[]{}"
                )

                if len(clean) > 5:
                    if clean not in keywords:
                        keywords.append(clean)


            keyword_text = ", ".join(
                keywords[:20]
            )


            if language == "తెలుగు":

                keyword_text = GoogleTranslator(
                    source="auto",
                    target="te"
                ).translate(keyword_text)


            elif language == "हिन्दी":

                keyword_text = GoogleTranslator(
                    source="auto",
                    target="hi"
                ).translate(keyword_text)


            st.success(keyword_text)



# -------------------------
# RESUME MATCHER
# -------------------------

elif feature == t["resume"]:

    st.subheader(t["resume"])


    resume = st.text_area(
        "Paste Resume"
    )


    job = st.text_area(
        "Paste Job Description"
    )


    if resume and job:


        resume_words = set(
            resume.lower().split()
        )

        job_words = set(
            job.lower().split()
        )


        score = (
            len(resume_words & job_words)
            /
            len(job_words)
        ) * 100


        st.metric(
            "Match Score",
            f"{score:.2f}%"
        )


        if score > 60:
            st.success("🎯 Good Match")

        elif score > 30:
            st.warning("⚠️ Partial Match")

        else:
            st.error("❌ Low Match")
