from dotenv import load_dotenv
load_dotenv()  # Automatically load environment variables from .env

import os
from openai import AzureOpenAI

def init_azure_openai_client():
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("API_VERSION")
    deployment_name = os.getenv("DEPLOYMENT_NAME")
    
    if not api_key or not endpoint:
        raise ValueError("AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT must be set in your .env file")
    if not api_version:
        raise ValueError("API_VERSION must be set in your .env file")
    if not deployment_name:
        raise ValueError("DEPLOYMENT_NAME must be set in your .env file")
    
    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version,
        azure_deployment=deployment_name  # Pre-configure the deployment name
    )
    return client

def create_azure_chat_completion(prompt, system_message=None, max_tokens=150,
                                 temperature=0.7, top_p=1.0, frequency_penalty=0.0,
                                 presence_penalty=0.0, stop=None):
    client = init_azure_openai_client()
    
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})
    
    # When using a pre-configured deployment, the model parameter can be set to a placeholder.
    response = client.chat.completions.create(
        model="<ignored>",  # This parameter is ignored because azure_deployment is set
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )
    return response.choices[0].message.content.strip()
