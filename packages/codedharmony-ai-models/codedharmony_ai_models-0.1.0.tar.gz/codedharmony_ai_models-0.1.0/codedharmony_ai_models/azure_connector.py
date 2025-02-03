from dotenv import load_dotenv
load_dotenv() 

import os
from openai import AzureOpenAI

def init_azure_openai_client():
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getnev("API_VERSION")
    if not api_key or not endpoint:
        raise ValueError("AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT must be set in your .env file")
    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version  
    )
    return client

def create_azure_chat_completion(prompt, max_tokens=150):
    client = init_azure_openai_client()
    deployment_name = os.getenv("DEPLOYMENT_NAME")
    if not deployment_name:
        raise ValueError("DEPLOYMENT_NAME must be set in your .env file")
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()
