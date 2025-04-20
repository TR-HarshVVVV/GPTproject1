#!/bin/bash

echo "Starting ngrok to make your application publicly accessible..."
echo ""
echo "Make sure your Flask application is running on port 5000"
echo ""
echo "Press Ctrl+C to stop ngrok when you're done"
echo ""

ngrok http 5000 