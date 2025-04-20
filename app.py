from flask import Flask, render_template, request, jsonify
import requests
import json
from database import ChatDatabase

# Initialize Flask app
app = Flask(__name__)
db = ChatDatabase()

# Ollama API base URL
OLLAMA_API_BASE = "http://localhost:11434/api"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/models', methods=['GET'])
def get_models():
    try:
        response = requests.get(f"{OLLAMA_API_BASE}/tags")
        response.raise_for_status()
        models = response.json().get('models', [])
        return jsonify({"models": [model['name'] for model in models]})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Could not connect to Ollama. Make sure Ollama is running locally."}), 500

@app.route('/chats', methods=['GET'])
def get_chats():
    try:
        chats = db.get_all_chats()
        return jsonify({"chats": chats})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chats/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    try:
        chat = db.get_chat(chat_id)
        if chat:
            return jsonify(chat)
        return jsonify({"error": "Chat not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chats', methods=['POST'])
def create_chat():
    try:
        data = request.json
        title = data.get('title', 'New Chat')
        model = data.get('model', 'mistral')
        chat_id = db.create_chat(title, model)
        return jsonify({"chat_id": chat_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chats/<int:chat_id>/messages', methods=['POST'])
def add_message(chat_id):
    try:
        data = request.json
        role = data.get('role')
        content = data.get('content')
        message_id = db.add_message(chat_id, role, content)
        return jsonify({"message_id": message_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chats/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    try:
        db.delete_chat(chat_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data['message']
        model = data.get('model', 'mistral')
        chat_id = data.get('chat_id')
        
        # Ollama API endpoint
        url = f"{OLLAMA_API_BASE}/generate"
        
        # Prepare the request payload
        payload = {
            "model": model,
            "prompt": user_message,
            "stream": False
        }
        
        # Make request to Ollama
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        ai_response = result.get('response', '')
        
        # Save messages to database if chat_id is provided
        if chat_id:
            db.add_message(chat_id, 'user', user_message)
            db.add_message(chat_id, 'assistant', ai_response)
        
        return jsonify({"response": ai_response})
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")  # For debugging
        return jsonify({"error": "Could not connect to Ollama. Make sure Ollama is running locally."}), 500
    except Exception as e:
        print(f"Error: {str(e)}")  # For debugging
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True) 