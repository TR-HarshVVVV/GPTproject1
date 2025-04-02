from flask import Flask, render_template, request, jsonify
import requests
import json

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        
        # Ollama API endpoint
        url = "http://localhost:11434/api/generate"
        
        # Prepare the request payload
        payload = {
            "model": "mistral",  # Using Mistral model
            "prompt": user_message,
            "stream": False
        }
        
        # Make request to Ollama
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the response
        result = response.json()
        ai_response = result.get('response', '')
        
        return jsonify({"response": ai_response})
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")  # For debugging
        return jsonify({"error": "Could not connect to Ollama. Make sure Ollama is running locally."}), 500
    except Exception as e:
        print(f"Error: {str(e)}")  # For debugging
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True) 