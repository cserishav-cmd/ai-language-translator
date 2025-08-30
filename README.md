# AI-Powered Language Hub 🤖

A modern, full-stack web application for real-time translation and language assistance, powered by the Google Gemini AI API and a Python Flask backend.

### [ ➡️ VIDEO ⬅️ ]



## ✨ Key Features

* **Real-Time AI Translation**: Instantly translate text between numerous languages using the powerful Gemini model.
* **Intelligent Suggestions**: Get real-time sentence completion and typo correction suggestions as you type.
* **Synonyms & Meanings**: Select any text to get a detailed breakdown of synonyms, definitions, and usage examples.
* **Voice-to-Text**: Use your microphone to speak directly into the app for quick and easy input.
* **Text-to-Speech**: Listen to the translated text with the click of a button.
* **Translation History**: Automatically saves your recent translations for quick reference.
* **Favorites**: Save important or frequently used translations to a dedicated favorites tab.
* **Dark Mode**: A sleek, eye-friendly dark mode for comfortable use in low-light conditions.
* **Responsive UI**: A clean and modern user interface built with Tailwind CSS that works on any device.

## 🛠️ Technologies Used

* **Backend**: Python, Flask
* **AI Model**: Google Gemini 1.5 Flash
* **Database**: SQLite
* **Frontend**: HTML, Tailwind CSS, JavaScript
* **Deployment**: Gunicorn, Render

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

* Python 3.8+
* Git for cloning the repository

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-folder>
    ```

2.  **Create a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create an environment file:**
    Create a new file named `.env` in the root of your project folder. Add your Google AI API key to this file.
    ```
    GOOGLE_AI_API_KEY="YOUR_API_KEY_HERE"
    ```

5.  **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

## 🌐 Deployment

This application is ready to be deployed on any platform that supports Python WSGI applications. It can be easily deployed for free on **Render**.

The key deployment settings are:
* **Build Command**: `pip install -r requirements.txt`
* **Start Command**: `gunicorn app:app`

Remember to add your `GOOGLE_AI_API_KEY` as an environment variable in your hosting provider's settings.

## 📁 File Structure
├── templates/
│   └── index.html      # Frontend user interface
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
├── .gitignore          # Files to be ignored by Git
└── README.md           # Project documentation
