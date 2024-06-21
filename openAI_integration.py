from openai import AsyncOpenAI

class OpenAIIntegration:
    def __init__(self, api_key: str, setup: str):
        self.api_key = api_key
        self.message_history = [{"role": "user", "content": setup}]
        self.client = AsyncOpenAI(api_key=self.api_key)
        
    
    async def chat(self, prompt: str):
        self.message_history.append({"role": "user", "content": prompt})
        
        completion = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.message_history,
            max_tokens=150
        )
        response = completion.choices[0].message.content.strip() if completion.choices else ""
        self.message_history.append({"role": "assistant", "content": response})
        
        return response