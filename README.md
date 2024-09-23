# GPT-Explainer Project Overview

## Introduction
**GPT-Explainer** is a Python-based application designed to help users understand PowerPoint presentations by generating explanations for each slide using the GPT-3.5 AI model. The project provides a solution for students or developers who find it challenging to comprehend presentation content by offering AI-powered, slide-by-slide explanations.

## Project Architecture
The project is composed of three key components:
1. **Explainer**: Responsible for processing PowerPoint files and generating explanations for each slide using OpenAI's GPT model.
2. **API**: Facilitates communication with the OpenAI API, sending slide text and receiving the AI's responses.
3. **Client**: A user-friendly console application that allows interaction with the system.

## Running the Application
To run the project, follow these steps:
1. **Navigate** to the main directory containing the Server and Client folders.
2. Open three separate command prompt windows:
   - In the first window, run the explainer:
     ```bash
     python .\Server\main_Explainer.py
     ```
     You will be prompted to enter your OpenAI API key.
   - In the second window, run the API service:
     ```bash
     python .\Server\main_API.py
     ```
   - In the third window, run the client:
     ```bash
     python .\Client\main.py
     ```
3. The client offers a choice between colored and uncolored console versions.

## Client Usage
The client application provides a console interface. You can explore available commands and their functions by typing the `help` command.

## Key Features
- **Asynchronous Execution**: The project uses Python’s `asyncio` for asynchronous API calls, reducing the wait time for responses.
- **Error Handling**: If an error occurs while processing a slide, the program continues processing the other slides and logs the error for the problematic slide.
- **CLI Interface**: The program can be run from the command line, with various options handled through `argparse`.
- **System Test**: Includes a pytest-based system test that verifies the output of the explainer script using a demo presentation file.

## Example Use
An example demonstration of the project in action can be viewed [here](https://www.youtube.com/watch?v=G-un4N4wH3o).

![344714216-49146165-cb01-409a-800c-a2024bd2d5c1](https://github.com/user-attachments/assets/3894f7c6-52ba-4eaa-8524-233387dd16bb)
## Requirements
- **Python Packages**: The project uses libraries such as `asyncio`, `python-pptx` for parsing PowerPoint files, and the `openai` package for API communication.
- **OpenAI API Key**: The system requires an OpenAI API key for generating explanations.

## Bonus Features
- **Timeout for Requests**: A timeout is implemented for OpenAI API requests to prevent long waits.
- **Slide Parsing**: The script ignores slides without text and handles irregular whitespaces within text.
- **Environment Variable for API Key**: The OpenAI API key is stored as a permanent environment variable.

## Future Enhancements
Potential features for further development include adding more robust error logging and enhancing the CLI for more user-friendly interactions.

---

This project brings together Python’s powerful libraries and OpenAI’s language models to simplify the process of understanding complex presentations by offering quick, AI-generated explanations.

