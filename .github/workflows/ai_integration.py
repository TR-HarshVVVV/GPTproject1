import openai
import os

# Fetch the API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenAI API credentials
openai.api_key = api_key

# Example API call to OpenAI's GPT-3 (replace with your own prompt)
response = openai.Completion.create(
  engine="text-davinci-003",
  prompt="Translate the following English text to French: 'Hello, how are you?'",
  max_tokens=50
)

# Print the translated text
print(response.choices[0].text.strip())
