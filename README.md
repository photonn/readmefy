# READMEFY

## Description
This repository contains a Python script designed to automate the generation of README.md files for code directories using the Azure OpenAI API. The script assesses all code files within a specified directory, dynamically constructs a detailed documentation prompt, and leverages OpenAI's API to generate a comprehensive README.md file.

## Prerequisites
To effectively use this repository, the following prerequisites are required:
- Python 3.8 or higher.
- Access to Azure OpenAI services with a valid API key.
- Installation of necessary Python packages like `openai`, `tiktoken`, and `python-dotenv`.

## Structure
The repository is structured into two main parts:
- **Code Files:**  
  - `readmefy.py`: The primary Python script which contains functions to identify code files, read their contents, construct the prompt, and interact with the Azure OpenAI API to generate the README.md file.

- **Mock Directory:**  
  - Contains a dummy HTML file (`main.py`) simulating a simple HTML webpage to demonstrate the script's capability to include various file types.

### Special Attention to Pipelines
The script primarily operates as a single-stage pipeline:
- **Trigger:** Initiated manually by running the script with a path argument on the command line.
- **Main Phases:**
  1. **File Scanning:** Identifying eligible code files based on predefined file extensions.
  2. **Content Aggregation:** Reading and assembling contents of the identified files.
  3. **Prompt Construction:** Formulating a complete documentation request from the aggregated content.
  4. **OpenAI API Interaction:** Sending the prompt to OpenAI and retrieving the generated README.md content.
  5. **File Creation:** Writing the received README.md content back to the specified directory.

## Usage
To generate a README for a directory:
1. Configure your `.env` file with necessary API configurations such as `AZURE_OPENAI_API_KEY`, `API_BASE`, etc.
2. Simply run the script as follows:
   ```bash
   python readmefy.py <PATH TO YOUR DIRECTORY>
   ```
   Replace `<PATH TO YOUR DIRECTORY>` with the path to the directory for which you want a README generated.

## Limitations
- **Token Limit:** The script is configured to handle prompts up to 128,000 tokens, which limits the amount of content that can be processed in a single request.
- **File Type Coverage:** While the script includes a comprehensive list of file extensions, unforeseen file types or files with no extensions might be ignored.
- **Error Handling:** The system primarily prints error messages to the console and does not recover or retry upon failures. 

This automated system simplifies the documentation process, ensuring consistent and detailed README files for varied software projects.