from dotenv import load_dotenv
load_dotenv() 

import os
import openai

def init_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key
    return openai

def create_chat_completion(prompt, model=os.getenv("OPENAI_MODEL"), max_tokens=150):
    client = init_openai_client()
    response = client.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()
