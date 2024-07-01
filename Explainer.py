import asyncio
from AIpptx import AIpptx
import time
import os


'''
added spacial features of understanding each slide
with the information of the slides & all the slides before  
'''
class __:
    '''
        Here you can change the main settings of this program:
    '''
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'outputs'
    
    INPUT_PPTX_PATH = "presentation.pptx"
    API_KEY = "sk-proj-xl0wdyeVmaJa2cneHXKvT3BlbkFJ1fGKvhcm74mM94u4j1Pr"
    MAX_SLIDES_ALLOWED = 10
    
    AI_SETUP = """You are a powerpoint slide explainer, but you can only read the text content of the slides (not the pictures).
    You will get the content of the slides, try to make sense of the information an understand what the idea of the slide.
    after you make sense of the slide, explain it, do it in away that is understandable clear and not long. 
    """

def get_unprocessed_files():
    processed_files = set(os.listdir(__.OUTPUT_FOLDER))
    all_files = os.listdir(__.UPLOAD_FOLDER)
    
    return [f for f in all_files if f.replace('pptx', 'json') not in processed_files]

def get_output_filepath(path):
    return path.replace(__.UPLOAD_FOLDER, __.OUTPUT_FOLDER).replace('.pptx', '.json')
    
async def upload_to_output_process(file_path):
    ai_pptx = AIpptx(__.API_KEY, file_path)
    await ai_pptx.run_on_slides_with_setup(__.MAX_SLIDES_ALLOWED, __.AI_SETUP)
    ai_pptx.save_json_file(get_output_filepath(file_path))


async def main():
    os.makedirs(__.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(__.OUTPUT_FOLDER, exist_ok=True)

    '''here's where you start this program'''
    #the prints make this main self explanatory
    while True:
        unprocessed_files = get_unprocessed_files()
        for filename in unprocessed_files:
            print('found -', filename)
            file_path = os.path.join(__.UPLOAD_FOLDER, filename)
            print('process -', filename)
            await upload_to_output_process(file_path)
            print('done -', filename)
            
        time.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
