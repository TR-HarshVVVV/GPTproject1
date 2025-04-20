@echo off
echo Ollama Chat Web - Deployment Script

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found. Please create one with your MongoDB connection string.
    exit /b 1
)

REM Build Docker image
echo Building Docker image...
docker build -t ollama-chat-web .

REM Run Docker container
echo Starting Docker container...
docker run -d -p 5000:5000 --env-file .env --name ollama-chat ollama-chat-web

echo Application deployed successfully!
echo Access it at http://localhost:5000
echo.
echo To make it publicly accessible, you can use ngrok:
echo 1. Install ngrok from https://ngrok.com/download
echo 2. Run: ngrok http 5000
echo 3. Share the provided URL with others 