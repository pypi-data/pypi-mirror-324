# codedharmony-ai-models

**codedharmony-ai-models** is a Python package that provides a unified interface for connecting to and interacting with various AI model services—such as OpenAI and Azure OpenAI—using prebuilt functions. By abstracting the connection and interaction logic into reusable functions, this package makes it easy to integrate advanced AI capabilities into your projects while minimizing boilerplate code and simplifying maintenance.

## Overview

Instead of writing repetitive code to initialize API clients, manage credentials, and handle API responses for each service separately, **codedharmony-ai-models** offers dedicated functions that:
- Initialize and configure clients for both OpenAI and Azure OpenAI.
- Load sensitive configuration from environment variables (using a `.env` file).
- Send chat or completion requests with consistent parameters.
- Return parsed responses for immediate use in your application.

Centralizing these responsibilities leads to:
- **Convenience:** Call a single function (e.g., `create_chat_completion()`) without worrying about setting up clients or managing credentials repeatedly.
- **Consistency:** A uniform interface to both OpenAI and Azure OpenAI minimizes the learning curve.
- **Maintainability:** Updates (such as API version changes) need only be made in one place.
- **Security:** Using a `.env` file (and the `python-dotenv` package) allows you to keep sensitive data out of your source code.


## Installation

Install the package using pip (once published to PyPI):

```bash
pip install codedharmony-ai-models
```




## Environment Setup

To keep your API keys and endpoints secure, create a `.env` file in the root of your project with the required variables. For example:

```env
# .env file
# For OpenAI API (if used)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=your_model_name

# For Azure OpenAI Service
AZURE_OPENAI_API_KEY=your_azure_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
DEPLOYMENT_NAME=your_deployment_name_here
API_VERSION=api_version
```


**Important:**

- Add the .env file to your .gitignore to prevent accidentally committing sensitive information.
- The package automatically loads these variables by calling load_dotenv() (from the python-dotenv package) during initialization. Ensure that you have installed this dependency:

```bash
pip install python-dotenv
```




## Usage Examples

### Using the OpenAI Connector

The **OpenAI connector** provides functions to set up and call the OpenAI API easily. For example:

```python
# File: example_openai.py
from codedharmony_ai_models.openai_connector import create_chat_completion

# Read a prompt from the user
prompt = input("Ask question for OpenAI: ")

# Define a system message for context
system_message = "You are a knowledgeable assistant specializing in artificial intelligence."

# Create a chat completion using the OpenAI API
response_text = create_chat_completion(
    prompt,
    system_message=system_message,
    max_tokens=200,      # Adjust maximum tokens as needed
    temperature=0.8,     # Control the creativity of the response
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=None            # Optionally set stop sequences
)

print("OpenAI response:", response_text)


```

### Using the Azure OpenAI Connector

The **Azure OpenAI connector** works similarly but is tailored for Azure’s deployment model. Ensure you have set the environment variables AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT before running:

```python
# File: example_azure.py
from codedharmony_ai_models.azure_connector import create_azure_chat_completion

# Read a prompt from the user
prompt = input("Ask question for Azure OpenAI: ")

# Define a system message for context
system_message = "You are a helpful expert in cloud-based AI services."

# Create a chat completion using Azure OpenAI Service
response_text = create_azure_chat_completion(
    prompt,
    system_message=system_message,
    max_tokens=200,      # Customize as needed
    temperature=0.8,     # Adjust for more or less randomness
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=None            # Optionally specify stop sequences
)

print("Azure OpenAI response:", response_text)


```


## Why Use This Package?

Using codedharmony-ai-models offers several key advantages over manually integrating AI APIs:

### Convenience:
The package centralizes the connection logic so that you simply call a function (e.g., create_chat_completion()) without having to set up API clients and manage credentials throughout your code.

### Consistency:
Both OpenAI and Azure OpenAI are accessed through a similar interface. This uniformity reduces the learning curve and minimizes the chance for errors when switching between services.

### Maintainability:
Updates to API versions or connection details only need to be made in one place (inside the connector modules), rather than scattered throughout your project. This decouples your business logic from low-level API details.

### Flexibility:
The abstraction allows you to easily switch endpoints or even add support for additional AI model providers in the future without refactoring your entire codebase.

### Simplified Error Handling:
By encapsulating API calls within dedicated functions, you can standardize error handling and logging, making it easier to debug issues compared to handling raw HTTP responses.