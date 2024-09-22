from openai import AsyncOpenAI
import asyncio

class OpenAIChat:
    def __init__(self, api_key: str, setup: str):
        """
        Initializes the OpenAIChat object.

        Args:
            api_key (str): The API key for OpenAI.
            setup (str): The setup-prompt for the AI chat.
        """

        self.api_key = api_key
        self.message_history = [{"role": "user", "content": setup}]
        self.client = AsyncOpenAI(api_key=self.api_key)
        
    async def chat(self, prompt: str):
        """
        Add a prompt to the chat with OpenAI.

        Args:
            prompt (str): The prompt to add to the chat.

        Returns:
            str: The response generated by OpenAI based on the prompt and older prompts from this chat.
        """

        self.message_history.append({"role": "user", "content": prompt})

        try:
            completion = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.message_history,
                    max_tokens=150
                ),
                timeout=5  # Specify the timeout value in seconds
            )
            response = completion.choices[0].message.content.strip() if completion.choices else ""
        except asyncio.TimeoutError:
            response = "Timeout occurred while waiting for the response from OpenAI."

        self.message_history.append({"role": "assistant", "content": response})

        return response