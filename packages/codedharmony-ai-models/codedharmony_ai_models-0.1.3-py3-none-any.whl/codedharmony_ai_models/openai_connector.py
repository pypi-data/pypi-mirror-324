from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

import os
import openai

def init_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set in your .env file")
    
    openai.api_key = api_key
    return openai

def create_chat_completion(prompt, max_tokens=150):
    client = init_openai_client()
    model = os.getenv("OPENAI_MODEL")
    if not model:
        raise ValueError("OPENAI_MODEL must be set in your .env file")
    
    response = client.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()
