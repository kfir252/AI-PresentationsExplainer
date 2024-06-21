import asyncio
from aipptx_json import AIpptx

class SETTINGS:
    '''
        Here you can change the main setting of the program
    '''
    
    INPUT_PPTX_PATH = "presentation.pptx"
    
    API_KEY = "sk-proj-xl0wdyeVmaJa2cneHXKvT3BlbkFJ1fGKvhcm74mM94u4j1Pr"
    MAX_SLIDES_ALLOWED = 10
    OUTPUT_JSON_FILE = "slide_responses.json"
    
    AI_SETUP = """You are a powerpoint slide explainer, but you can only read the text content of the slides (not the pictures).
    You will get the content of the slides, try to make sense of the information an understand what the idea of the slide.
    after you make sense of the slide, explain it, do it in away that is understandable clear and not long. 
    """

async def main():
    print('Reading-The-Presentation', end='', flush=True)
    ai_pptx = AIpptx(SETTINGS.API_KEY, SETTINGS.INPUT_PPTX_PATH)
    print('[DONE]')
    
    print('Processing-With-AI (may take a minute)', end='', flush=True)
    await ai_pptx.run_on_slides_with_setup(SETTINGS.MAX_SLIDES_ALLOWED, SETTINGS.AI_SETUP)
    print('[DONE]')
    
    ai_pptx.save_json_file(SETTINGS.OUTPUT_JSON_FILE)
    print('Output Ready At:' ,SETTINGS.OUTPUT_JSON_FILE)

if __name__ == "__main__":
    asyncio.run(main())
