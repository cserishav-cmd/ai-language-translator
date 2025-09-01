# 🌍 AI-Powered Language Hub 🤖

A modern, full-stack web application for **real-time translation and language assistance**, powered by the **Google Gemini AI API** and a **Python Flask backend**.

---

## 🎥 Demo Video
[ ➡️ [VIDEO LINK HERE](https://youtu.be/dJffZv6-cl4) ⬅️ ]

---

## ✨ Features

- **🌐 Real-Time AI Translation** – Instantly translate text between multiple languages using **Gemini 1.5 Flash**.
- **💡 Intelligent Suggestions** – Get sentence completion, typo correction, and context-aware suggestions.
- **📚 Synonyms & Meanings** – Select any text to see synonyms, definitions, and usage examples.
- **🎤 Voice-to-Text** – Speak directly into the app and convert speech into text.
- **🔊 Text-to-Speech** – Listen to translated text in natural voice.
- **📜 Translation History** – Automatically saves recent translations for quick access.
- **⭐ Favorites** – Save important or frequently used translations.
- **🌙 Dark Mode** – Eye-friendly UI for comfortable late-night usage.
- **📱 Responsive UI** – Built with **Tailwind CSS**, optimized for all devices.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask  
- **AI Model**: Google Gemini 1.5 Flash  
- **Database**: SQLite  
- **Frontend**: HTML, Tailwind CSS, JavaScript  
- **Deployment**: Gunicorn, Render  

---

## 🚀 Getting Started

### Prerequisites
- Python **3.8+**
- Git installed on your system

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd <repository-folder>
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**  
   Create a `.env` file in the root directory:
   ```ini
   GOOGLE_AI_API_KEY="YOUR_API_KEY_HERE"
   ```

5. **Run the app**
   ```bash
   flask run
   ```
   Visit 👉 `http://127.0.0.1:5000`

---

## 🌐 Deployment

This app can be deployed on any **Python WSGI-compatible platform** (e.g., Render, Heroku, Railway).

**Render Example Setup:**
- **Build Command:**  
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command:**  
  ```bash
  gunicorn app:app
  ```
- Add `GOOGLE_AI_API_KEY` in **Render Environment Variables**.

---

## 📁 Project Structure

```
├── templates/
│   └── index.html      # Frontend UI
├── static/             # (Optional) CSS/JS assets
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
├── .env                # API key (not committed to Git)
├── .gitignore          # Ignore sensitive/unnecessary files
└── README.md           # Documentation
```

---

## 🙌 Contribution

Contributions are welcome! Feel free to fork this repo and submit PRs with improvements.

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify it.

---
