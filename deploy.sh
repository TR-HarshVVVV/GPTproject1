#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please create one with your MongoDB connection string."
    exit 1
fi

# Build Docker image
echo "Building Docker image..."
docker build -t ollama-chat-web .

# Run Docker container
echo "Starting Docker container..."
docker run -d -p 5000:5000 --env-file .env --name ollama-chat ollama-chat-web

echo "Application deployed successfully!"
echo "Access it at http://localhost:5000"
echo ""
echo "To make it publicly accessible, you can use ngrok:"
echo "1. Install ngrok from https://ngrok.com/download"
echo "2. Run: ngrok http 5000"
echo "3. Share the provided URL with others" 