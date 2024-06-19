import aiohttp
import asyncio

class OpenAIIntegration:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.openai.com/v1/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    async def send_to_openai_api(self, prompt):
        """
        Sends text to OpenAI's API asynchronously and returns the response.

        Args:
            prompt (str): Text to send as a prompt.

        Returns:
            str: Response text from OpenAI API.
        """
        payload = {
            "model": "text-davinci-003",  # Adjust to your preferred model
            "prompt": prompt,
            "max_tokens": 150  # Adjust token limit based on your needs
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint, json=payload, headers=self.headers) as response:
                response_json = await response.json()
                return response_json["choices"][0]["text"].strip()


