# -*- coding: utf-8 -*-
"""
Iya Bola Assistant App
Dataverse Datathon 2025
----------------------------------------
Run locally:
    streamlit run Banking_Iya_Bola_App.py
Requirements:
    streamlit, pandas, fasttext
    Optional: gTTS, SpeechRecognition, langdetect
----------------------------------------
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import fasttext
import plotly.express as px
import requests
import base64
import os

# ---------------------------------------------------
# INITIAL PAGE CONFIG (run once per session)
# ---------------------------------------------------
if "page_configured" not in st.session_state:
    st.set_page_config(page_title="Iya Bola Assistant", page_icon="💬", layout="wide")
    st.session_state["page_configured"] = True

st.title("💬 Iya Bola Assistant")
st.caption("Inclusive Financial Assistant for Africa — Text/Voice based Prototype")

# ---------------------------------------------------
# OPTIONAL LIBRARIES
# ---------------------------------------------------
try:
    import speech_recognition as sr
    from gtts import gTTS
except ImportError:
    sr = None
    gTTS = None

if "log" not in st.session_state:
    st.session_state["log"] = []

# ---------------------------------------------------
# LOAD FASTTEXT LANGUAGE DETECTION MODEL
# ---------------------------------------------------
@st.cache_resource
def load_lang_model():
    try:
        model = fasttext.load_model("language_detect.ftz")
        st.success("✅ Language model loaded successfully.")
        return model
    except Exception as e:
        st.warning(f"⚠️ Could not load ML language model: {e}")
        return None

lang_model = load_lang_model()

# ---------------------------------------------------
# LANGUAGE AND SETTINGS
# ---------------------------------------------------
st.markdown("### 🌐 Gender & Language Settings")

gender_spec = st.radio(
    "Select your gender identity:",
    ("Male", "Female"),
    horizontal=True
)

language_choice = st.radio(
    "Select your preferred language:",
    ("Auto-detect", "English", "Pidgin", "Yoruba"),
    horizontal=True
)

voice_lang = st.selectbox(
    "🎙️ Choose voice input language:",
    {
        "English (Nigeria)": "en-NG",
        "Yoruba": "yo",
        "Pidgin (use English base)": "en-NG"
    },
    index=0
)

# ---------------------------------------------------
# LANGUAGE DETECTION
# ---------------------------------------------------
def detect_language(user_input):
    """Detect language based on user preference or ML classification."""
    if language_choice != "Auto-detect":
        return language_choice

    if lang_model:
        try:
            prediction = lang_model.predict(user_input)
            label = prediction[0][0].replace("__label__", "")
            if label in ("pcm","Pidgin","pidgin","pijin","pigin"):
                label = "Pidgin"
            elif label in ("Yoruba","yo","yoruba"):
                label = "Yoruba"
            elif label in ("English","en","english"):
                label = "English"
            return label
        except Exception:
            pass

    text = user_input.lower()
    if any(word in text for word in ["oya", "abeg", "wahala", "dey", "wan", "una", "papa", "wetin"]):
        return "Pidgin"
    elif any(word in text for word in ["ba mi","fi","bawo", "e kaaro", "se", "ni", "elo", "ranse", "fun mi"]):
        return "Yoruba"
    else:
        return "English"

# ---------------------------------------------------
# INTENT CLASSIFICATION
# ---------------------------------------------------
def classify_intent(message):
    msg = message.lower()
    if any(x in msg for x in ["balance", "account", "check", "wetin dey", "wetin remain", "ki lo ku", "oye to ku"]):
        return "Account Balance"
    elif any(x in msg for x in ["send", "pay", "credit", "transfer", "give", "wan send","ranse", "ranse si"]):
        return "Money Transfer"
    elif any(x in msg for x in ["buy airtime", "recharge", "data","ra data"]):
        return "Airtime / Data Purchase"
    elif any(x in msg for x in ["bill", "light", "pay nepa", "dstv","owo ina"]):
        return "Bill Payment"
    elif any(x in msg for x in ["save", "keep", "contribute","pamo","hold","holam","hol"]):
        return "Micro-Savings"
    elif any(x in msg for x in ["teach", "how to", "explain", "meaning","ko mi","mo fe mo"]):
        return "Financial Education"
    else:
        return "General Chat"

# ---------------------------------------------------
# RESPONSE GENERATOR
# ---------------------------------------------------
def generate_response(message, language, intent):
    responses = {
        "Account Balance": {
            "en": "✅ Your account balance is ₦xxx,yyy.zz. 💸",
            "pcm": "✅ Ya account balance bin ₦xxx,yyy.zz. 💸",
            "yo": "✅ Oye to ku ninu apo ifowopamo re ni ₦xxx,yyy.zz. 💸",
        },
        "Money Transfer": {
            "en": "✅ Transaction successful! ₦2,000 has been sent. 💸",
            "pcm": "✅ Di transfer don go! You don send ₦2,000. 💸",
            "yo": "✅ Ìsanwó ṣáájú! O ti fi ₦2,000 ránṣẹ́. 💸",
        },
        "Airtime / Data Purchase": {
            "en": "📱 Airtime top-up complete. You’ve been credited with ₦500!",
            "pcm": "📱 Airtime don enter! You don get ₦500 credit!",
            "yo": "📱 Airtime rẹ ti wáyé! ₦500 ti jẹ́ kó tó ọ́!",
        },
        "Bill Payment": {
            "en": "💡 Your NEPA bill has been paid successfully.",
            "pcm": "💡 You don pay your NEPA bill sharp sharp.",
            "yo": "💡 Ìsanwó NEPA rẹ ti péye.",
        },
        "Micro-Savings": {
            "en": "💰 Great! ₦1,000 saved to your micro-savings account.",
            "pcm": "💰 Correct! ₦1,000 don enter your savings.",
            "yo": "💰 Dáadáa! ₦1,000 ti fi pamọ́ sí àkọọlẹ̀ ipamọ́ rẹ.",
        },
        "Financial Education": {
            "en": "📖 Tip: Always save at least 10% of your income monthly.",
            "pcm": "📖 Tip: Try save small-small every month, like 10%.",
            "yo": "📖 Ìmòràn: Máa fi 10% owó-oṣù rẹ pamọ́ lẹ́ẹ̀kan oṣù.",
        },
        "General Chat": {
            "en": "👋 I'm happy to assist with your financial tasks anytime!",
            "pcm": "👋 I dey always ready to help you with your money mata!",
            "yo": "👋 Inú mi dùn láti ran ọ́ lọ́wọ́ nípa ìṣúná rẹ!",
        },
    }

    resp = responses.get(intent, responses["General Chat"])
    if language in ("English","en","EN"):
        return resp.get(language, resp["en"])
    if language in ("Yoruba","yo"):
        return resp.get(language, resp["yo"])
    if language in ("Pidgin","pcm"):
        return resp.get(language, resp["pcm"])

# ---------------------------------------------------
# SPEECH RECOGNITION
# ---------------------------------------------------
def recognize_speech():
    if sr is None:
        st.warning("🎧 SpeechRecognition not installed.")
        return ""

    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info(f"🎙️ Listening in {voice_lang}...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            text = recognizer.recognize_google(audio, language=voice_lang)
            st.success(f"You said: {text}")
            return text
    except AttributeError:
        st.error("🎧 Audio not found. Speech recognition unavailable on this platform.")
    except OSError:
        st.error("🚫 No microphone detected. Please check your audio device.")
    except sr.UnknownValueError:
        st.error("🤔 Sorry, I couldn't understand that.")
    except sr.RequestError:
        st.error("⚠️ Speech service unavailable or selected language not supported.")
    except Exception as e:
        st.error(f"⚙️ Unexpected audio error: {str(e)}")
    return ""

# ---------------------------------------------------
# TEXT-TO-SPEECH
# ---------------------------------------------------
def speak_text(response_text, language):
    hf_models = {
        "yo": "facebook/mms-tts-yor",
        "pcm": "facebook/mms-tts-pcm",
        "en": "facebook/mms-tts-eng"
    }

    # Select the right model ID
    if language in ("English", "en", "EN"):
        model_id = hf_models["en"]
        language = "en"
    elif language in ("Yoruba", "yo"):
        model_id = hf_models["yo"]
        language = "yo"
    elif language in ("Pidgin", "pcm"):
        model_id = hf_models["pcm"]
        language = "pcm"
    else:
        model_id = hf_models["en"]
        language = "en"

    token = os.getenv("HF_TOKEN")

    try:
        # --- Try Hugging Face TTS first ---
        if not token:
            raise ValueError("Missing HF_TOKEN. Using fallback gTTS.")

        resp = requests.post(
            f"https://api-inference.huggingface.co/models/{model_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"inputs": response_text}
        )
        resp.raise_for_status()
        result = resp.json()

        # Ensure 'audio' exists
        if "audio" not in result:
            raise ValueError("No audio field returned from Hugging Face model.")

        audio_data = base64.b64decode(result["audio"])
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        with open(temp.name, "wb") as f:
            f.write(audio_data)
        st.audio(temp.name, format="audio/mp3")

    except Exception:
        # --- Fallback to gTTS ---
        if gTTS is None:
            st.warning("Speech unavailable: gTTS not installed or failed to import.")
            return

        lang_code = {"yo": "en", "pcm": "en", "en": "en"}.get(language, "en")
        try:
            tts = gTTS(text=response_text, lang=lang_code)
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tmp.name)
            st.audio(tmp.name, format="audio/mp3")
        except Exception as e:
            st.error(f"Speech unavailable: {e}")



# ---------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------
col1, col2 = st.columns([2, 1])

# --- CHAT WINDOW ---
with col1:
    st.subheader("💬 Chat Window")
    user_input = st.text_input(
        "Type your message below 👇",
        placeholder="E.g., I wan send 2k go my mama account",
        key="user_input_box"
    )

    # Ensure a flag to prevent duplicate logging
    if "last_logged_input" not in st.session_state:
        st.session_state["last_logged_input"] = None

    # Speech button
    if st.button("🎙️ Speak Instead"):
        user_input = recognize_speech()

    # Send button logic (log only once per new message)
    if st.button("Send") and user_input:
        if user_input != st.session_state["last_logged_input"]:
            language = detect_language(user_input)
            intent = classify_intent(user_input)
            response = generate_response(user_input, language, intent)

            st.session_state["log"].append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_input": user_input,
                "language": language,
                "intent": intent,
                "response": response,
                "gender": gender_spec
            })

            st.session_state["last_logged_input"] = user_input  # ✅ store last input
            st.info(f"🗣️ Language used: {language}")
            st.success(response)
            speak_text(response, language)
        else:
            st.warning("⚠️ You already sent this message.")


st.subheader("📊 Real-Time Dashboard")

# Check for log data
if st.session_state.get("log"):
    df = pd.DataFrame(st.session_state["log"])

    # Ensure timestamp column exists and convert to datetime
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # --- FILTERS ---
    st.markdown("### 🔍 Filter Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_gender = st.selectbox(
            "Filter by Gender", 
            options=["All"] + sorted(df["gender"].dropna().unique().tolist())
        )
    with col2:
        selected_intent = st.selectbox(
            "Filter by Intent", 
            options=["All"] + sorted(df["intent"].dropna().unique().tolist())
        )
    with col3:
        selected_language = st.selectbox(
            "Filter by Language", 
            options=["All"] + sorted(df["language"].dropna().unique().tolist())
        )

    # --- DATE RANGE FILTER ---
    if "timestamp" in df.columns and not df["timestamp"].isna().all():
        min_date = df["timestamp"].min().date()
        max_date = df["timestamp"].max().date()
        st.markdown("#### 📅 Filter by Date Range")
        start_date, end_date = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    else:
        start_date, end_date = None, None

    # --- APPLY FILTERS ---
    filtered_df = df.copy()
    if selected_gender != "All":
        filtered_df = filtered_df[filtered_df["gender"] == selected_gender]
    if selected_intent != "All":
        filtered_df = filtered_df[filtered_df["intent"] == selected_intent]
    if selected_language != "All":
        filtered_df = filtered_df[filtered_df["language"] == selected_language]
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df["timestamp"].dt.date >= start_date)
            & (filtered_df["timestamp"].dt.date <= end_date)
        ]

    # --- CHARTS ---
    st.markdown("### 📈 Insights Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Intent Distribution")
        st.bar_chart(filtered_df["intent"].value_counts())

    with col2:
        st.markdown("#### Language Usage")
        st.bar_chart(filtered_df["language"].value_counts())

    with col3:
        st.markdown("#### Gender Inclusion")
        gender_counts = filtered_df["gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]

        if not gender_counts.empty:
            fig = px.pie(
                gender_counts,
                values="Count",
                names="Gender",
                title="Gender Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textinfo="percent+label", pull=[0.05]*len(gender_counts))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No gender data available for current filters.")

    # --- LAST 10 INTERACTIONS ---
    st.markdown("### 🧾 Last 10 Interactions (Filtered)")
    st.dataframe(filtered_df.tail(10), use_container_width=True)

    # --- DOWNLOAD BUTTON ---
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered Log (CSV)",
        data=csv,
        file_name="iya_bola_filtered_log.csv",
        mime="text/csv"
    )

else:
    st.info("No logs found yet. Start interacting to generate dashboard data.")