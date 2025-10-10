#### 💬 Iya Bola Assistant App - Streamlit Prototype

**Inclusive Financial Assistant for Africa — Dataverse Datathon 2025 Submission**
Iya Bola Assistant is a multilingual, data-driven financial assistant designed to empower underserved communities across Africa.  
It supports essential financial tasks and provides financial education using simple, conversational interactions in **English**, **Pidgin**, and **Yoruba**.

###### 

#### 🧩 Files Structure

###### **📁 iya-bola-assistant/**

├── Banking\_Iya\_Bola\_App.py     # Streamlit prototype

├── requirements.txt            # Dependencies

├── README.md                   # Documentation

├── project\_overview.md         # Datathon submission overview

└── sample\_user\_log.csv         # Mock chat data for analytics demo



#### 🧩 Installations:

1. Core (Required): pip install streamlit pandas langdetect
2. Voice Features: pip install SpeechRecognition gTTS pyaudio
3. Voice input/output will only work if these are installed.



#### ▶️ Local Installation \& Running:

1. **Clone or download** the project folder.
   ```bash
   git clone https://github.com/<your-username>/iya-bola-assistant.git
   cd iya-bola-assistant
2. **Install Dependencies:**
pip install -r requirements.txt
3. **Run the App:**
   streamlit run Banking\_Iya\_Bola\_App.py
   The app will launch automatically in your browser at: http://localhost:8501

   ###### 🧠 Tech Stack

   * [Python 3.8+](https://www.python.org/downloads/)
   * [Streamlit](https://streamlit.io/)
   * [Pandas](https://pandas.pydata.org/)
   * [NumPy](https://numpy.org/)

4. Interact with the app through text or voice
   e.g. "check my balance"


☁️ Live Demo (Hosted on Streamlit Cloud)

4. 🔗 Click to open live demo
   (Replace with your actual deployment link once live)



#### 📊 Analytics Output:

   The dashboard visualizes:

1. Frequency of user intents (e.g. savings, airtime, transfers)
2. Frequency of language usage (English, Pidgin, Yoruba)
3. All chat logs are automatically stored in memory and can be downloaded as CSV file using the "download chat logs" button.



#### 🚀 Features:

* **Multilingual Chatbot:** Understands English, Pidgin, and Yoruba keywords.
* **Core Financial Tasks:** Simulates balance checks, transfers, bill payments, airtime/data purchases, and micro-savings.
* **Financial Education:** Offers savings and budgeting tips in simple language.
* **Analytics Dashboard:** Real-time bar charts for user intents and language distribution.
* **Downloadable Logs:** Exports all chat data to CSV for Power BI or further analysis.



#### 💡 Future Enhancements:

⦁	Add GPT API backend for smarter natural responses
⦁	Integrate Firebase or SQLite for permanent chat storage
⦁	Power BI dashboard from CSV.
Add Hausa, Igbo, or Swahili samples for broader coverage.
Split data into train.txt / valid.txt to report precision \& recall.
Log a small confusion matrix to include in usage report.



#### Impact \& Scalability

1. The solution can integrate with banks, fintechs, and telcos to extend digital financial access.
2. Its modular, multilingual design makes it scalable across new regions and local languages.



## 👤 Author

Ope Sadiku — GrandMEAN Analytics
🔗 LinkedIn: https://www.linkedin.com/in/opeyemi-sadiku-514094327

for Dataverse Datathon 2025

   

