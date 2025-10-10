# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 00:30:12 2025

@author: EBUNOLUWASIMI
"""

# IYA BOLA ASSISTANT
# Streamlit prototype: text + optional voice + live dashboard

import streamlit as st
from langdetect import detect
import pandas as pd
from datetime import datetime
import tempfile

# Optional voice libraries
try:
    import speech_recognition as sr
    from gtts import gTTS
except ImportError:
    sr = None
    gTTS = None

st.set_page_config(page_title="Banking Iya Bola App", page_icon="💬", layout="wide")

st.title("🤖 Iya Bola Assistant")
st.caption("Empowering Africa through Data-Driven Inclusion 🌍")

# ---------------------------------
# LANGUAGE SELECTION SECTION
# ---------------------------------
st.markdown("### 🌐 Language Settings")

language_choice = st.radio(
    "Select your preferred language:",
    ("Auto-detect", "English", "Pidgin", "Yoruba"),
    horizontal=True
)

def detect_language(user_input):
    """
    Detect language based on user preference or heuristics.
    """
    if language_choice != "Auto-detect":
        # User manually selected a language
        return language_choice

    # Automatic detection (fallback)
    try:
        lang_code = detect(user_input)
    except:
        lang_code = "unknown"

    # Heuristic keyword-based improvement for African languages
    text = user_input.lower()
    if any(word in text for word in ["oya", "abeg", "wahala", "dey"]):
        return "Pidgin"
    elif any(word in text for word in ["bawo", "e kaaro", "se", "ni"]):
        return "Yoruba"
    elif lang_code.startswith("en"):
        return "English"
    else:
        return "English"  # default fallback

if "log" not in st.session_state:
    st.session_state["log"] = []

def classify_intent(message):
    msg = message.lower()
    if any(x in msg for x in ["send", "transfer", "give", "wan send"]):
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

def generate_response(message, language, intent):
    responses = {
        "Money Transfer": "✅ Transaction successful! ₦2,000 has been sent. 💸",
        "Airtime / Data Purchase": "📱 Airtime top-up complete. You’ve been credited with ₦500!",
        "Bill Payment": "💡 Your NEPA bill has been paid successfully.",
        "Micro-Savings": "💰 Great! ₦1,000 saved to your micro-savings account.",
        "Financial Education": "📖 Financial Tip: Always save at least 10% of your income monthly.",
        "General Chat": "👋 I'm happy to assist with your financial tasks anytime!"
    }

    if language == "yo":
        responses = {k: v.replace("Your", "Ìwọ̀n rẹ") for k, v in responses.items()}
    elif language == "pcm":
        responses = {k: v.replace("Your", "Ya own") for k, v in responses.items()}

    return responses.get(intent, responses["General Chat"])

def recognize_speech():
    if sr is None:
        st.warning("🎧 Audio feature not installed. Speech recognition unavailable.")
        return ""

    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎙️ Listening... please speak now")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text

    except AttributeError:
        # Happens when PyAudio is missing (e.g. Streamlit Cloud)
        st.error("🎧 Audio not found. Speech recognition unavailable on this platform.")
    except OSError:
        # Happens when no microphone device is present
        st.error("🚫 No microphone detected. Please check your audio device.")
    except sr.UnknownValueError:
        st.error("🤔 Sorry, I couldn't understand that.")
    except sr.RequestError:
        st.error("⚠️ Speech service unavailable.")
    except Exception as e:
        # Catch any unexpected errors without crashing
        st.error(f"⚙️ Unexpected audio error: {str(e)}")

    return ""


def speak_text(response_text):
    # Handle missing or unavailable gTTS library
    if gTTS is None:
        st.warning("🔇 Text-to-speech not installed. Voice playback unavailable.")
        return

    try:
        # Attempt to generate speech
        tts = gTTS(text=response_text, lang="en")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        st.audio(temp_file.name, format="audio/mp3")

    except AssertionError:
        # Sometimes raised if text is empty or invalid
        st.warning("⚙️ Nothing to speak — the response text is empty.")
    except ValueError as ve:
        # Invalid language or TTS parameters
        st.error(f"🌐 Text-to-speech error: {ve}")
    except OSError:
        # Happens when the server cannot connect to Google TTS
        st.error("🌐 Network issue: could not reach text-to-speech service.")
    except Exception as e:
        # Catch-all for any other unexpected errors
        st.error(f"⚙️ Voice generation error: {str(e)}")

col1, col2 = st.columns([2,1])

with col1:
    st.subheader("💬 Chat Window")
    user_input = st.text_input("Type your message below 👇", placeholder="E.g., I wan send 2k go my mama account")
    if st.button("🎙️ Speak Instead"):
        user_input = recognize_speech()
    if st.button("Send") or user_input:
        if user_input:
            try:
                language = detect_language(user_input)
            except:
                language = "unknown"
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
        st.download_button("⬇️ Download Log (CSV)", data=csv, file_name="iya_bola_chat_log.csv", mime="text/csv")
    else:
        st.info("No chats yet. Start a conversation!")
