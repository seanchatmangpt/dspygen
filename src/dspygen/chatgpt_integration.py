import openai
import os
from dotenv import load_dotenv

# Load environments variables from .env file
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

def send_message_to_chatgpt(message):
    """
    Sends a message to OpenAI's GPT-3.5-turbo model and returns the response.
    """
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant"},
            {"role": "user", "content": message}
        ]
    )

    response_message = completion['choices'][0]['message']['content']
    return response_message.strip()
