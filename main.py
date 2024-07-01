
import asyncio
from AIpptx import AIpptx

'''
added spacial features of understanding each slide
with the information of the slides & all the slides before  
'''

class SETTINGS:
    '''
        Here you can change the main settings of this program:
    '''
    
    INPUT_PPTX_PATH = "presentation.pptx"
    OUTPUT_JSON_PATH = ''.join(INPUT_PPTX_PATH.split('.')[:-1]) + '.json'
    API_KEY = "sk-proj-xl0wdyeVmaJa2cneHXKvT3BlbkFJ1fGKvhcm74mM94u4j1Pr"
    MAX_SLIDES_ALLOWED = 10
    
    AI_SETUP = """You are a powerpoint slide explainer, but you can only read the text content of the slides (not the pictures).
    You will get the content of the slides, try to make sense of the information an understand what the idea of the slide.
    after you make sense of the slide, explain it, do it in away that is understandable clear and not long. 
    """

async def main():
    '''here's where you start this program'''
    #the prints make this main self explanatory
    
    print('Reading-The-Presentation', end='', flush=True)
    ai_pptx = AIpptx(SETTINGS.API_KEY, SETTINGS.INPUT_PPTX_PATH)
    print('[DONE]')
    
    print('Processing-With-AI (may take some time)', end='', flush=True)
    await ai_pptx.run_on_slides_with_setup(SETTINGS.MAX_SLIDES_ALLOWED, SETTINGS.AI_SETUP)
    print('[DONE]')
    
    ai_pptx.save_json_file(SETTINGS.OUTPUT_JSON_PATH)
    print('Output Ready At:' ,SETTINGS.OUTPUT_JSON_PATH)

if __name__ == "__main__":
    asyncio.run(main())
