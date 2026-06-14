import streamlit as st
import PyPDF2
from deep_translator import GoogleTranslator

try:
    import ollama
    ollama_available = True
except:
    ollama_available = False


st.set_page_config(
    page_title="Smart PDF & Career Assistant",
    layout="wide"
)


# -------------------------
# LANGUAGE SUPPORT
# -------------------------

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
    [
        "English",
        "తెలుగు",
        "हिन्दी"
    ]
)


t = translations[language]


st.title(t["title"])


# -------------------------
# AI MODE
# -------------------------

ai_mode = st.sidebar.selectbox(
    "🤖 AI Mode",
    [
        "Built-in AI",
        "Local AI (Ollama)",
        "BYOK"
    ]
)


api_key = ""

if ai_mode == "BYOK":

    api_key = st.sidebar.text_input(
        "Enter your AI API Key",
        type="password"
    )


# -------------------------
# AI SUMMARY FUNCTION
# -------------------------
# -------------------------
# AI SUMMARY FUNCTION
# -------------------------

def generate_summary(text):

    # Local AI using Ollama
    if ai_mode == "Local AI (Ollama)":

        if ollama_available:

            try:

                response = ollama.chat(
                    model="llama3",
                    messages=[
                        {
                            "role": "user",
                            "content":
                            f"Summarize this document clearly:\n{text}"
                        }
                    ]
                )

                return response["message"]["content"]


            except Exception:

                return (
                    "Ollama is not connected. "
                    "Please run Ollama locally with a model "
                    "to use Local AI inference."
                )


        else:

            return (
                "Ollama package is not available. "
                "Install Ollama to use Local AI."
            )


    # BYOK option
    elif ai_mode == "BYOK":

        if api_key:

            return (
                "BYOK mode selected. "
                "Your API token is accepted. "
                "Connect your preferred AI provider here."
            )

        else:

            return (
                "Please enter your API key "
                "to use BYOK mode."
            )


    # Default built-in AI
    else:

        summary = " ".join(
            text.split()[:200]
        )

        return summary

# -------------------------
# FEATURE SELECTION
# -------------------------

feature = st.sidebar.selectbox(
    "Choose Feature",
    [
        t["pdf"],
        t["resume"]
    ]
)
# -------------------------
# SMART PDF SIMPLIFIER
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

            st.write(
                "## 📊 Document Statistics"
            )


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


            # AI Summary

            st.write(
                "## 📝 Smart Summary"
            )


            summary = generate_summary(text)


            # Translation

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

            st.write(
                "## 🎯 Important Keywords"
            )


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


    st.subheader(
        t["resume"]
    )


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



        if len(job_words) > 0:


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

                st.success(
                    "🎯 Good Match"
                )


            elif score > 30:

                st.warning(
                    "⚠️ Partial Match"
                )


            else:

                st.error(
                    "❌ Low Match"
                )
