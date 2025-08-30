import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('GOOGLE_AI_API_KEY')

DATABASE = 'translator.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_lang TEXT NOT NULL,
                source_text TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_lang TEXT NOT NULL,
                source_text TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        db.commit()
        db.close()

try:
    if not API_KEY:
        raise ValueError("GOOGLE_AI_API_KEY not found")
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print("Gemini model configured successfully")
    
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    if not model:
        return jsonify({
            "error": "Gemini model is not initialized"
        }), 500

    try:
        data = request.json
        text = data.get('text')
        source_lang = data.get('source_lang')
        target_lang = data.get('target_lang')
        
        if not text or not source_lang or not target_lang:
            return jsonify({"error": "Missing required fields"}), 400
        
        prompt = f"Translate the following text from {source_lang} to {target_lang}. Return only the translated plain text without any explanations or additional content:\n\n{text}"
        
        response = model.generate_content(prompt, request_options={"timeout": 60})
        
        if not response.parts:
            block_reason = "Unknown"
            if response.prompt_feedback:
                block_reason = response.prompt_feedback.block_reason
            raise ValueError(f"Response was blocked. Reason: {block_reason}")
        
        translated_text = response.text.strip()
        
        db = get_db()
        db.execute(
            'INSERT INTO history (source_lang, source_text, target_lang, translated_text) VALUES (?, ?, ?, ?)',
            (source_lang, text, target_lang, translated_text)
        )
        db.commit()
        db.close()
        
        return jsonify({"translated_text": translated_text})
        
    except Exception as e:
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500

@app.route('/suggest', methods=['POST'])
def get_suggestions():
    if not model:
        return jsonify({"error": "Gemini model is not initialized."}), 500
    
    try:
        data = request.json
        text = data.get('text')
        language = data.get('language')
        
        if not text or not language:
            return jsonify({"error": "Missing required fields"}), 400
        
        if len(text.strip()) < 3:
            return jsonify([])

        prompt = f"""You are an intelligent writing assistant. Based on the following partial text in {language}, provide up to 3 helpful suggestions. The suggestions can be either to complete the sentence or to correct a typo.

Rules:
- Your entire response must be a valid JSON array of strings.
- Do not include any other text, explanations, or markdown formatting.
- If no suggestions are needed, return an empty array [].

Partial Text: "{text}"
"""
        
        response = model.generate_content(prompt, request_options={"timeout": 15})
        
        if not response.parts:
            return jsonify([])

        suggestions_text = response.text.strip()
        
        try:
            suggestions = json.loads(suggestions_text)
            if not isinstance(suggestions, list):
                raise ValueError("Response is not a list")
            return jsonify(suggestions)
        except (json.JSONDecodeError, ValueError):
            return jsonify([])

    except Exception as e:
        return jsonify({"error": f"Failed to get suggestions: {str(e)}"}), 500

@app.route('/synonyms', methods=['POST'])
def get_synonyms():
    if not model:
        return jsonify({"error": "Gemini model is not initialized."}), 500
    
    try:
        data = request.json
        text = data.get('text')
        language = data.get('language')
        
        if not text or not language:
            return jsonify({"error": "Missing required fields"}), 400
        
        prompt = f"""For the {language} word/phrase '{text}', provide a detailed analysis including:

### Synonyms
List alternative words or phrases with similar meanings.

### Definitions
Provide clear definitions and explanations.

### Usage Examples
Show how the word/phrase can be used in different contexts.

Format your response in markdown with proper headings and bullet points."""
        
        response = model.generate_content(prompt, request_options={"timeout": 60})
        
        if not response.parts:
            block_reason = "Unknown"
            if response.prompt_feedback:
                block_reason = response.prompt_feedback.block_reason
            raise ValueError(f"Response was blocked. Reason: {block_reason}")
        
        synonyms_text = response.text.strip()
        
        return jsonify({"synonyms_text": synonyms_text})
        
    except Exception as e:
        return jsonify({"error": f"Failed to get synonyms: {str(e)}"}), 500

@app.route('/history', methods=['GET'])
def get_history():
    try:
        db = get_db()
        history_cursor = db.execute(
            'SELECT * FROM history ORDER BY timestamp DESC LIMIT 50'
        )
        history = [dict(row) for row in history_cursor.fetchall()]
        db.close()
        
        return jsonify(history)
        
    except Exception as e:
        return jsonify({"error": f"Failed to get history: {str(e)}"}), 500

@app.route('/favorites', methods=['GET', 'POST'])
def handle_favorites():
    db = get_db()
    
    try:
        if request.method == 'GET':
            fav_cursor = db.execute('SELECT * FROM favorites ORDER BY id DESC')
            favorites = [dict(row) for row in fav_cursor.fetchall()]
            db.close()
            
            return jsonify(favorites)
        
        elif request.method == 'POST':
            data = request.json
            
            required_fields = ['source_lang', 'source_text', 'target_lang', 'translated_text']
            for field in required_fields:
                if not data.get(field):
                    db.close()
                    return jsonify({"error": f"Missing required field: {field}"}), 400
            
            existing = db.execute(
                'SELECT id FROM favorites WHERE source_lang = ? AND source_text = ? AND target_lang = ?',
                (data['source_lang'], data['source_text'], data['target_lang'])
            ).fetchone()
            
            if existing:
                db.close()
                return jsonify({
                    "success": False,
                    "message": "This translation is already saved",
                    "duplicate": True
                }), 200
            
            db.execute(
                'INSERT INTO favorites (source_lang, source_text, target_lang, translated_text) VALUES (?, ?, ?, ?)',
                (data['source_lang'], data['source_text'], data['target_lang'], data['translated_text'])
            )
            db.commit()
            new_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
            db.close()
            
            return jsonify({"success": True, "id": new_id, "message": "Added to favorites!"}), 201
            
    except Exception as e:
        db.close()
        return jsonify({"error": f"Favorites operation failed: {str(e)}"}), 500

@app.route('/favorites/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    try:
        db = get_db()
        
        favorite = db.execute('SELECT * FROM favorites WHERE id = ?', (id,)).fetchone()
        if not favorite:
            db.close()
            return jsonify({"error": "Favorite not found"}), 404
        
        db.execute('DELETE FROM favorites WHERE id = ?', (id,))
        db.commit()
        db.close()
        
        return jsonify({"success": True}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to delete favorite: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "model_initialized": model is not None,
        "api_key_configured": API_KEY is not None,
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

init_db()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)