import re
from collections import Counter

import PyPDF2
import streamlit as st
from deep_translator import GoogleTranslator

try:
    import ollama

    ollama_available = True
except ImportError:
    ollama_available = False


st.set_page_config(page_title="Smart PDF & Career Assistant", layout="wide")


LANGUAGES = {
    "English": {
        "title": "📄 Smart PDF & Career Assistant",
        "choose_language": "Choose Language",
        "choose_feature": "Choose Feature",
        "pdf": "Smart PDF Simplifier",
        "resume": "Resume Matcher",
        "upload": "Upload a PDF File",
        "pdf_success": "✅ PDF processed successfully",
        "pdf_error": "❌ Could not read this PDF.",
        "stats": "📊 Document Statistics",
        "pages": "Pages",
        "words": "Words",
        "reading_time": "Reading Time",
        "minutes": "min",
        "summary": "📝 Short Summary",
        "key_points": "🔑 Key Points",
        "keywords": "🎯 Important Keywords",
        "study_questions": "❓ Study Questions",
        "paste_resume": "Paste Resume",
        "paste_job": "Paste Job Description",
        "match_score": "Match Score",
        "good_match": "🎯 Good Match",
        "partial_match": "⚠️ Partial Match",
        "low_match": "❌ Low Match",
        "empty_pdf": "⚠️ No readable text found in the PDF.",
        "summary_unavailable": "Summary not available.",
        "no_keywords": "No important keywords found.",
        "q1": "1. What is the main topic of this document?",
        "q2": "2. Which concepts are most important?",
        "q3": "3. What conclusions are presented?",
        "q4": "4. What should a student remember?",
        "q5": "5. Which areas need further study?",
        "how_it_helps": "This tool gives a quick summary, key points, keywords, and study questions from the uploaded PDF.",
    },
    "తెలుగు": {
        "title": "📄 స్మార్ట్ PDF & కెరీర్ అసిస్టెంట్",
        "choose_language": "భాషను ఎంచుకోండి",
        "choose_feature": "ఫీచర్‌ను ఎంచుకోండి",
        "pdf": "స్మార్ట్ PDF సరళీకరణ",
        "resume": "రెజ్యూమ్ మ్యాచర్",
        "upload": "PDF ఫైల్‌ను అప్లోడ్ చేయండి",
        "pdf_success": "✅ PDF విజయవంతంగా ప్రాసెస్ చేయబడింది",
        "pdf_error": "❌ ఈ PDF ను చదవలేకపోయాం.",
        "stats": "📊 పత్ర గణాంకాలు",
        "pages": "పేజీలు",
        "words": "పదాలు",
        "reading_time": "చదివే సమయం",
        "minutes": "నిమి",
        "summary": "📝 చిన్న సారాంశం",
        "key_points": "🔑 ముఖ్యాంశాలు",
        "keywords": "🎯 ముఖ్య కీవర్డ్స్",
        "study_questions": "❓ చదువు ప్రశ్నలు",
        "paste_resume": "రెజ్యూమ్‌ను పేస్ట్ చేయండి",
        "paste_job": "జాబ్ వివరణను పేస్ట్ చేయండి",
        "match_score": "మ్యాచ్ స్కోర్",
        "good_match": "🎯 మంచి మ్యాచ్",
        "partial_match": "⚠️ భాగంగా మ్యాచ్",
        "low_match": "❌ తక్కువ మ్యాచ్",
        "empty_pdf": "⚠️ PDF లో చదవగలిగే టెక్స్ట్ కనిపించలేదు.",
        "summary_unavailable": "సారాంశం అందుబాటులో లేదు.",
        "no_keywords": "ముఖ్యమైన కీవర్డ్స్ కనబడలేదు.",
        "q1": "1. ఈ పత్రం యొక్క ప్రధాన విషయం ఏమిటి?",
        "q2": "2. అత్యంత ముఖ్యమైన కాన్సెప్ట్‌లు ఏమిటి?",
        "q3": "3. ఇందులో ఏ నిర్ణయాలు చెప్పబడ్డాయి?",
        "q4": "4. విద్యార్థి గుర్తుంచుకోవాల్సిన అంశాలు ఏమిటి?",
        "q5": "5. ఇంకా ఏ అంశాలు చదవాలి?",
        "how_it_helps": "ఈ సాధనం అప్లోడ్ చేసిన PDF నుండి చిన్న సారాంశం, ముఖ్యాంశాలు, కీవర్డ్స్, చదువు ప్రశ్నలను ఇస్తుంది.",
    },
    "हिन्दी": {
        "title": "📄 स्मार्ट PDF और करियर असिस्टेंट",
        "choose_language": "भाषा चुनें",
        "choose_feature": "फ़ीचर चुनें",
        "pdf": "स्मार्ट PDF सरलकर्ता",
        "resume": "रिज़्यूमे मैचर",
        "upload": "PDF फ़ाइल अपलोड करें",
        "pdf_success": "✅ PDF सफलतापूर्वक प्रोसेस हो गई",
        "pdf_error": "❌ यह PDF पढ़ी नहीं जा सकी।",
        "stats": "📊 दस्तावेज़ आँकड़े",
        "pages": "पेज",
        "words": "शब्द",
        "reading_time": "पढ़ने का समय",
        "minutes": "मिनट",
        "summary": "📝 छोटा सारांश",
        "key_points": "🔑 मुख्य बिंदु",
        "keywords": "🎯 महत्वपूर्ण कीवर्ड्स",
        "study_questions": "❓ अध्ययन प्रश्न",
        "paste_resume": "रिज़्यूमे पेस्ट करें",
        "paste_job": "जॉब डिस्क्रिप्शन पेस्ट करें",
        "match_score": "मैच स्कोर",
        "good_match": "🎯 अच्छा मैच",
        "partial_match": "⚠️ आंशिक मैच",
        "low_match": "❌ कम मैच",
        "empty_pdf": "⚠️ PDF में पढ़ने योग्य टेक्स्ट नहीं मिला।",
        "summary_unavailable": "सारांश उपलब्ध नहीं है।",
        "no_keywords": "कोई महत्वपूर्ण कीवर्ड नहीं मिला।",
        "q1": "1. इस दस्तावेज़ का मुख्य विषय क्या है?",
        "q2": "2. सबसे महत्वपूर्ण अवधारणाएँ कौन-सी हैं?",
        "q3": "3. इसमें कौन-से निष्कर्ष दिए गए हैं?",
        "q4": "4. छात्र को क्या याद रखना चाहिए?",
        "q5": "5. किन क्षेत्रों में आगे अध्ययन की आवश्यकता है?",
        "how_it_helps": "यह टूल अपलोड की गई PDF से छोटा सारांश, मुख्य बिंदु, कीवर्ड्स और अध्ययन प्रश्न देता है।",
    },
}


STOPWORDS = {
    "the",
    "and",
    "for",
    "that",
    "with",
    "this",
    "from",
    "have",
    "your",
    "you",
    "are",
    "was",
    "were",
    "has",
    "had",
    "will",
    "into",
    "their",
    "they",
    "them",
    "then",
    "than",
    "what",
    "when",
    "where",
    "which",
    "while",
    "about",
    "there",
    "these",
    "those",
    "been",
    "being",
    "also",
    "such",
    "using",
    "used",
    "through",
    "would",
    "could",
    "should",
    "very",
    "more",
    "some",
    "only",
    "most",
    "each",
    "other",
    "over",
    "under",
    "between",
    "into",
    "onto",
    "their",
    "his",
    "her",
    "our",
    "ours",
    "its",
    "it",
    "in",
    "on",
    "at",
    "of",
    "to",
    "a",
    "an",
    "is",
    "be",
    "or",
    "as",
    "by",
    "if",
    "not",
    "we",
    "he",
    "she",
    "i",
    "me",
    "my",
    "mine",
}


def translate_text(text: str, target_language: str) -> str:
    """Translate text to Telugu or Hindi if needed."""
    if not text.strip():
        return text

    if target_language == "English":
        return text

    lang_code = "te" if target_language == "తెలుగు" else "hi"

    try:
        # translate only smaller chunks to avoid API limits
        max_chars = 4000
        parts = []
        current = ""

        for paragraph in text.split("\n"):
            if len(current) + len(paragraph) + 1 <= max_chars:
                current += paragraph + "\n"
            else:
                parts.append(current.strip())
                current = paragraph + "\n"

        if current.strip():
            parts.append(current.strip())

        translated_parts = [
            GoogleTranslator(source="auto", target=lang_code).translate(part)
            for part in parts
            if part.strip()
        ]
        return "\n".join(translated_parts)
    except Exception:
        return text


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text: str) -> list[str]:
    raw_sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [clean_text(s) for s in raw_sentences if len(clean_text(s)) > 30]
    return sentences


def build_summary(text: str) -> str:
    sentences = split_sentences(text)
    if not sentences:
        return ""

    if ollama_available:
        try:
            prompt = (
                "Summarize the following document in 5-7 concise sentences. "
                "Focus on the main topic, important details, and conclusions.\n\n"
                f"{text[:12000]}"
            )
            response = ollama.chat(
                model="llama3.2",
                messages=[{"role": "user", "content": prompt}],
            )
            content = response["message"]["content"].strip()
            if content:
                return content
        except Exception:
            pass

    # fallback summary without AI
    return " ".join(sentences[:5])


def extract_key_points(text: str, max_points: int = 5) -> list[str]:
    sentences = split_sentences(text)
    return sentences[:max_points]


def extract_keywords(text: str, max_keywords: int = 15) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9\-\+\.]*", text.lower())
    filtered = [
        word
        for word in words
        if len(word) > 4 and word not in STOPWORDS and not word.isdigit()
    ]
    counts = Counter(filtered)
    return [word for word, _ in counts.most_common(max_keywords)]


def normalize_words(text: str) -> set[str]:
    tokens = re.findall(r"[a-zA-Z0-9+#.\-]+", text.lower())
    return {token for token in tokens if len(token) > 1}


# -------------------------
# Sidebar Language + Feature
# -------------------------

language = st.sidebar.selectbox("🌐 Language / भाषा / భాష", list(LANGUAGES.keys()))
t = LANGUAGES[language]

st.title(t["title"])

feature = st.sidebar.selectbox(
    t["choose_feature"],
    [t["pdf"], t["resume"]],
)

# -------------------------
# SMART PDF SIMPLIFIER
# -------------------------

if feature == t["pdf"]:
    st.subheader("📄 " + t["pdf"])
    st.caption(t["how_it_helps"])

    uploaded_file = st.file_uploader(t["upload"], type=["pdf"])

    if uploaded_file is not None:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            extracted_pages = []

            for page in reader.pages:
                extracted_pages.append(page.extract_text() or "")

            raw_text = "\n".join(extracted_pages).strip()

            if not raw_text:
                st.warning(t["empty_pdf"])
            else:
                words = raw_text.split()
                pages = len(reader.pages)
                word_count = len(words)
                reading_time = max(1, round(word_count / 200))

                summary = build_summary(raw_text) or t["summary_unavailable"]
                key_points = extract_key_points(raw_text)
                keywords = extract_keywords(raw_text)

                translated_summary = translate_text(summary, language)
                translated_points = [
                    translate_text(point, language) for point in key_points
                ]
                translated_keywords = [
                    translate_text(keyword, language) for keyword in keywords
                ]

                st.success(t["pdf_success"])

                st.write("## " + t["stats"])
                col1, col2, col3 = st.columns(3)
                col1.metric(t["pages"], pages)
                col2.metric(t["words"], word_count)
                col3.metric(t["reading_time"], f"{reading_time} {t['minutes']}")

                st.write("## " + t["summary"])
                st.info(translated_summary)

                st.write("## " + t["key_points"])
                if translated_points:
                    for point in translated_points:
                        st.write(f"• {point}")
                else:
                    st.write("• " + t["summary_unavailable"])

                st.write("## " + t["keywords"])
                if translated_keywords:
                    st.success(", ".join(translated_keywords))
                else:
                    st.warning(t["no_keywords"])

                st.write("## " + t["study_questions"])
                st.write(t["q1"])
                st.write(t["q2"])
                st.write(t["q3"])
                st.write(t["q4"])
                st.write(t["q5"])

        except Exception:
            st.error(t["pdf_error"])

# -------------------------
# RESUME MATCHER
# -------------------------

elif feature == t["resume"]:
    st.subheader("💼 " + t["resume"])

    resume = st.text_area(t["paste_resume"], height=220)
    job = st.text_area(t["paste_job"], height=220)

    if resume and job:
        resume_words = normalize_words(resume)
        job_words = normalize_words(job)

        if job_words:
            match_score = (len(resume_words & job_words) / len(job_words)) * 100
        else:
            match_score = 0.0

        st.metric(t["match_score"], f"{match_score:.2f}%")

        if match_score > 60:
            st.success(t["good_match"])
        elif match_score > 30:
            st.warning(t["partial_match"])
        else:
            st.error(t["low_match"])
