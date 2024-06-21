
import json
from openAI_integration import OpenAIIntegration
from pptx_parser import PresentationParser

class AIpptx:
    def __init__(self, api_key: str, pptx_path: str):
        self.api_key = api_key
        self.pptx_path = pptx_path
        self.slide_responses = []
        self.parser = PresentationParser(self.pptx_path)
    
    async def run_on_slides_with_setup(self, slide_count: int, setup:str):
        
        ai_agent = OpenAIIntegration(self.api_key, setup)
        
        slide_count = min(self.parser.total_slides, slide_count)
        
        for slide_index in range(1, slide_count + 1):
            if slide_data := self.parser.get_slide(slide_index):
                prompt = ' '.join(slide_data["content"]) 
                
                response = await ai_agent.chat(prompt)

                self.slide_responses.append({
                    "slide_number": slide_index,
                    "prompt": prompt,
                    "response": response
                    }) if prompt.strip() else self.slide_responses.append({
                    "slide_number": slide_index,
                    "prompt": "empty",
                    "response": "empty"
                    })

    
    def save_json_file(self, filename: str):
        try:
            with open(filename, 'w') as f:
                json.dump(self.slide_responses, f, indent=4)
        except Exception as e:
            print(f"Error saving JSON to file: {str(e)}")

