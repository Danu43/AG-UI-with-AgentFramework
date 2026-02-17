import requests
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
version = os.getenv("AZURE_OPENAI_VERSION")

# Safety cleanup
endpoint = endpoint.rstrip("/")

url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={version}"

print("Testing URL:", url)

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

data = {
    "messages": [
        {"role": "user", "content": "Hello"}
    ],
    "max_completion_tokens": 10
}

response = requests.post(url, headers=headers, json=data)

print("Status:", response.status_code)
print("Response:", response.text)
