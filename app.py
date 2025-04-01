from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OpenAI API key found in environment variables")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        
        # Get response from OpenAI using the newer API format
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        
        # Extract the assistant's response using the new format
        ai_response = response.choices[0].message.content
        
        return jsonify({"response": ai_response})
    
    except Exception as e:
        print(f"Error: {str(e)}")  # For debugging
        error_message = str(e)
        if "Invalid API key" in error_message:
            return jsonify({"error": "Invalid API key. Please check your API key in the .env file."}), 500
        elif "Rate limit" in error_message:
            return jsonify({"error": "Rate limit exceeded. Please try again later."}), 500
        else:
            return jsonify({"error": f"An error occurred: {error_message}"}), 500

if __name__ == '__main__':
    app.run(debug=True) 