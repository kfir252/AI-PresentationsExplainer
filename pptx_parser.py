from pptx import Presentation

class PresentationParser:
    def __init__(self, pptx_path):
        self.pptx_path = pptx_path
        self.presentation_data = None
    
    def parse_presentation(self):
        """
        Summary:
        Parse the content of a PowerPoint presentation.

        Explanation:
        Given a path to a PowerPoint presentation (pptx file), this method parses the slides and extracts the slide number, title, and content. It returns a list of dictionaries, each representing a slide with its slide number, title, and content.

        Returns:
            list: A list of dictionaries containing slide information.
        """
        presentation = Presentation(self.pptx_path)
        return [
            {
                "slide_number": slide_number,
                "title": title if (title := next((shape.text.strip() for shape in slide.shapes if hasattr(shape, 'text') and shape == slide.shapes.title), "")) else "",
                "content": [shape.text.strip() for shape in slide.shapes if hasattr(shape, 'text') and shape != slide.shapes.title]
            }
            for slide_number, slide in enumerate(presentation.slides, start=1)
        ]
    
    def print_presentation_data(self, presentation_data):
        """
        Summary:
        Print the parsed data of a presentation.

        Explanation:
        This method takes the parsed presentation data and prints the slide number, title, and content in a formatted manner. It iterates over the presentation data list and prints each slide's information.

        Args:
            presentation_data (list): A list of dictionaries containing parsed slide information.

        Returns:
            None
        """
        [print(f"Slide {slide_data['slide_number']}\nTitle: {slide_data['title']}\nContent:\n" + ''.join([f"- {content}\n" for content in slide_data['content']]) + '='*40 + '\n') for slide_data in presentation_data]

    
    def process_presentation(self, flag = 0):
        self.presentation_data = self.parse_presentation()
        if flag:
          self.print_presentation_data(self.presentation_data)

def main():
    PPTX_PATH = "C:\\Users\\kfirl\\Desktop\\presentation.pptx"
    parser = PresentationParser(PPTX_PATH)
    parser.process_presentation(1)

if __name__ == "__main__":
    main()
