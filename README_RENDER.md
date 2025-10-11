# 🌍 Iya Bola Assistant App (Render Deployment)

### Dataverse Datathon 2025 Submission
Developed by **Ope Sadiku | GrandMEAN Analytics**

---

## 🎯 Overview
**Iya Bola Assistant App** is a multilingual, multimodal financial assistant designed to promote financial inclusion in Africa.  
It helps users — especially those with low digital literacy — perform essential financial tasks like:
- 💸 Transfers  
- 💡 Bill Payments  
- 📱 Airtime/Data Purchases  
- 💰 Micro-savings  
- 📖 Financial Literacy Tips  

The assistant supports **English, Pidgin, and Yoruba**, and uses text + optional voice input/output.

---

## 🧠 Tech Stack
- **Python 3.10**
- **Streamlit**
- **Pandas**
- **langdetect**
- **SpeechRecognition** *(optional voice input)*
- **gTTS** *(optional text-to-speech output)*
- **PyAudio** *(required for microphone access)*

---

## 🛠️ Render Deployment Instructions

### 1️⃣ Repository Structure

📦 iya-bola-assistant/
├── Banking_Iya_Bola_App.py
├── requirements.txt
├── Dockerfile
├── project_overview.md
├── sample_user_log.csv
└── README.md

### 2️⃣ Requirements
Create `requirements.txt` with:

streamlit
pandas
langdetect
SpeechRecognition
gTTS
PyAudio
fasttext

### 3️⃣ Deploy on Render
1. Go to [https://render.com](https://render.com)
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Choose:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `bash start.sh`
   - **Environment:** Python 3.10
   - **Instance Type:** Free

## 🌐 Live Demo
Once deployed, your app will be accessible at:

https://<your-app-name>.onrender.com

https://iya-bola-assistant.onrender.com


🧠 Why Docker?
Benefit	Description
🧱 PortAudio support	Allows PyAudio to compile and enable real-time voice input/output
🗂️ Consistent environment	Everyone runs the same version of Python, Streamlit, and dependencies
🔒 Sandboxed security	App is isolated from the host system
🌍 Easy deployment	Runs identically on Render, AWS, or any cloud platform

🎯 Key Features (Docker Build)

✅ Text + Voice Chat using SpeechRecognition and gTTS

🌐 Multilingual Interface (English, Pidgin, Yoruba)

📊 Real-Time Analytics Dashboard (intent & language stats)

💾 Downloadable Logs for Power BI analysis

🧩 Modular ML Integration (FastText for language detection)

🚀 Running Locally (for developers)

You can also test the container locally if you have Docker installed:
---

## 🎤 Voice Features
If **PyAudio** fails to build, your app will gracefully fallback with:
> “🎧 Audio not found — Speech recognition unavailable.”

So the demo remains live even if microphone features aren’t supported on Render’s free instance.

---

## 🧾 Logs & Analytics
- All user messages and system responses are stored in a Pandas DataFrame
- Real-time charts show:
  - Intent distribution
  - Language detection breakdown
- Data exportable as CSV via `Download Log` button

---

## 🧠 Future Scalability
The architecture allows:
- FastText-based language model (option C)
- SMS/USSD integration
- Financial literacy modules via API
- Offline deployment for community banks

---

## 💡 Credits
Developed by **GrandMEAN Analytics (Ope Sadiku)**  
For **Dataverse Datathon 2025 – Financial Inclusion Challenge**
