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
#from langdetect import detect
import tempfile
import fasttext
#import os

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
# LANGUAGE SETTINGS
# ---------------------------------------------------
st.markdown("### 🌐 Language Settings")

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

def detect_language(user_input):
    """
    Detect language based on user preference or ML classification.
    """
    # Step 1: Respect user's manual choice
    if language_choice != "Auto-detect":
        return language_choice

    # Step 2: Try ML model if available
    if lang_model:
        try:
            prediction = lang_model.predict(user_input)
            label = prediction[0][0].replace("__label__", "")
            return label
        except Exception:
            pass

    # Step 3: Heuristic fallback (keyword-based)
    text = user_input.lower()
    if any(word in text for word in ["oya", "abeg", "wahala", "dey"]):
        return "Pidgin"
    elif any(word in text for word in ["bawo", "e kaaro", "se", "ni"]):
        return "Yoruba"
    else:
        return "English"

# ---------------------------------------------------
# INTENT CLASSIFICATION
# ---------------------------------------------------
def classify_intent(message):
    msg = message.lower()
    if any(x in msg for x in ["balance", "account", "check", "weytin dey"]):
        return "Account Balance"
    elif any(x in msg for x in ["send", "transfer", "give", "wan send"]):
        return "Money Transfer"
    elif any(x in msg for x in ["buy airtime", "recharge", "data"]):
        return "Airtime / Data Purchase"
    elif any(x in msg for x in ["bill", "light", "pay nepa", "dstv"]):
        return "Bill Payment"
    elif any(x in msg for x in ["save", "keep", "contribute"]):
        return "Micro-Savings"
    elif any(x in msg for x in ["teach", "how to", "explain", "meaning"]):
        return "Financial Education"
    else:
        return "General Chat"

# ---------------------------------------------------
# RESPONSE GENERATOR
# ---------------------------------------------------
def generate_response(message, language, intent):
    responses = {
        "Account Balance": "💰 Your Account Balance: ₦xxx,yyy.zz 💸",
        "Money Transfer": "✅ Transaction successful! ₦2,000 has been sent. 💸",
        "Airtime / Data Purchase": "📱 Airtime top-up complete. You’ve been credited with ₦500!",
        "Bill Payment": "💡 Your NEPA bill has been paid successfully.",
        "Micro-Savings": "💰 Great! ₦1,000 saved to your micro-savings account.",
        "Financial Education": "📖 Tip: Always save at least 10% of your income monthly.",
        "General Chat": "👋 I'm happy to assist with your financial tasks anytime!"
    }

    if language in ["Yoruba", "yo"]:
        responses = {k: v.replace("Your", "Ìwọ̀n rẹ") for k, v in responses.items()}
    elif language in ["Pidgin", "pcm"]:
        responses = {k: v.replace("Your", "Ya own") for k, v in responses.items()}

    return responses.get(intent, responses["General Chat"])

# ---------------------------------------------------
# SPEECH RECOGNITION (SAFE)
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
# TEXT-TO-SPEECH (SAFE)
# ---------------------------------------------------
def speak_text(response_text):
    if gTTS is None:
        st.warning("🔇 Text-to-speech not installed. Voice playback unavailable.")
        return

    try:
        tts = gTTS(text=response_text, lang="en")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        st.audio(temp_file.name, format="audio/mp3")

    except AssertionError:
        st.warning("⚙️ Nothing to speak — the response text is empty.")
    except ValueError as ve:
        st.error(f"🌐 Text-to-speech error: {ve}")
    except OSError:
        st.error("🌐 Network issue: could not reach text-to-speech service.")
    except Exception as e:
        st.error(f"⚙️ Voice generation error: {str(e)}")

# ---------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat Window")
    user_input = st.text_input("Type your message below 👇", placeholder="E.g., I wan send 2k go my mama account")

    if st.button("🎙️ Speak Instead"):
        user_input = recognize_speech()

    if st.button("Send") or user_input:
        if user_input:
            language = detect_language(user_input)
            intent = classify_intent(user_input)
            response = generate_response(user_input, language, intent)
            st.session_state["log"].append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_input": user_input,
                "language": language,
                "intent": intent,
                "response": response
            })
            st.info(f"🗣️ Language used: {language}")
            st.success(response)
            speak_text(response)

with col2:
    st.subheader("📊 Real-Time Dashboard")
    if st.session_state["log"]:
        df = pd.DataFrame(st.session_state["log"])
        st.write("### Intent Distribution")
        st.bar_chart(df["intent"].value_counts())
        st.write("### Language Usage")
        st.bar_chart(df["language"].value_counts())
        st.write("### Last 10 Interactions")
        st.dataframe(df.tail(10), use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Log (CSV)", data=csv,
                           file_name="iya_bola_chat_log.csv", mime="text/csv")
    else:
        st.info("No chats yet. Start a conversation!")
