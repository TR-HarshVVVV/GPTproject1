# Ollama Chat Web Interface

A web-based interface for testing and interacting with Ollama's AI models without installing them locally. This application provides a clean, modern chat interface similar to ChatGPT, allowing users to experiment with different Ollama models through a browser.

![Ollama Chat Screenshot](screenshot.png)

## Features

- **Multiple Model Support**: Test different Ollama models including Mistral, TinyLlama, and more
- **Chat History**: Save and manage your conversations
- **Modern UI**: Clean, responsive interface inspired by popular chat applications
- **MongoDB Integration**: Persistent storage for all your chats and messages
- **Real-time Responses**: Get immediate responses from the AI models

## Tech Stack

- **Frontend**:

  - HTML5, CSS3, JavaScript
  - Font Awesome for icons
  - Responsive design for all devices

- **Backend**:

  - Python 3.8+
  - Flask web framework
  - MongoDB for data storage
  - Ollama API integration

- **Deployment**:
  - Docker support
  - Environment variable configuration
  - MongoDB Atlas integration

## Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account (or local MongoDB instance)
- Ollama installed and running locally (for local development)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/ollama-chat-web.git
   cd ollama-chat-web
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your MongoDB connection string:

   ```
   MONGODB_URI=your_mongodb_connection_string
   ```

4. Start the Flask application:

   ```
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Docker Deployment

1. Build the Docker image:

   ```
   docker build -t ollama-chat-web .
   ```

2. Run the container:
   ```
   docker run -p 5000:5000 --env-file .env ollama-chat-web
   ```

## Making Your Application Publicly Accessible

To make your application accessible to others, you have several options:

### Option 1: Deploy to a Cloud Platform

1. **Heroku**:

   - Create a Heroku account
   - Install the Heroku CLI
   - Run `heroku create`
   - Add MongoDB add-on: `heroku addons:create mongolab`
   - Deploy: `git push heroku main`

2. **Render**:

   - Create a Render account
   - Connect your GitHub repository
   - Set environment variables
   - Deploy as a web service

3. **Railway**:
   - Create a Railway account
   - Connect your GitHub repository
   - Set environment variables
   - Deploy

### Option 2: Use a Reverse Proxy with ngrok

For temporary public access:

1. Install ngrok: https://ngrok.com/download
2. Start your Flask application
3. Run: `ngrok http 5000`
4. Share the provided URL with others

### Option 3: Deploy to a VPS

1. Rent a VPS (DigitalOcean, AWS EC2, etc.)
2. Set up Nginx as a reverse proxy
3. Configure SSL with Let's Encrypt
4. Deploy your application using Gunicorn or uWSGI

## Configuration for Public Deployment

When deploying publicly, make sure to:

1. Set `FLASK_ENV=production` in your environment variables
2. Use a production WSGI server like Gunicorn
3. Configure proper CORS settings if needed
4. Set up proper authentication if required
5. Use environment variables for all sensitive information

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
