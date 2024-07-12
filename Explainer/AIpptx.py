
import json
from OpenAIChat import OpenAIChat
from PresentationParser import PresentationParser

class AIpptx:
    def __init__(self, api_key: str, pptx_path: str):
        """
        Initializer for AIpptx
        
        Args:
            api_key (str): The API key for OpenAI.
            pptx_path (str): The path to the PowerPoint presentation file.
        """

        self.api_key = api_key
        self.pptx_path = pptx_path
        self.slide_responses = []
        self.parser = PresentationParser(self.pptx_path)
    
    async def run_on_slides_with_setup(self, slide_count: int, setup:str):
        """
        Runs an AI-chat on slides content with a given setup-prompt.

        Args:
            slide_count (int): The number of slides to run the AI chat on.
            setup (str): The setup-prompt for the AI chat.

        Returns:
            None
        """
        ai_agent = OpenAIChat(self.api_key, setup)
        
        if slide_count is None:
            slide_count = self.parser.total_slides
        else:
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
        """
        Saves the slide_responses to a JSON file.

        Args:
            filename (str): The path to the JSON file.

        Raises:
            Exception: If an error occurs while saving the JSON file.
        """

        try:
            with open(filename, 'w') as f:
                json.dump(self.slide_responses, f, indent=4)
        except Exception as e:
            print(f"Error saving JSON to file: {str(e)}")