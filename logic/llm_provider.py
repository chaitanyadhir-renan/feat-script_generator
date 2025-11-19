import os
import requests
from dotenv import load_dotenv


class LLM_provider:
    def __init__(self):
        # Load environment variables from .env in root
        load_dotenv(dotenv_path="/Users/chaitanyadhir/Renan/databrewery/script_generator/.env")
        

        # Azure OpenAI configuration loaded from environment variables
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    def call_llm(self, prompt):

        url = f"{self.azure_endpoint.rstrip('/')}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful script generator."},
                {"role": "user", "content": prompt}  # <-- your prompt string goes here
            ],
            # "max_tokens": 4096,  # The maximum for GPT-4o is 4096 tokens per output
            # "temperature": 0.7
        }

        resp = requests.post(url, headers=headers, json=data)

        if resp.status_code == 200:
            response_data = resp.json()
            return response_data["choices"][0]["message"]["content"]
        else:
            return f"Error: {resp.status_code}, {resp.text}"
