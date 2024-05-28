import os
import openai
from typing import List
import sys
import tiktoken
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration parameters
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
API_BASE = os.getenv('API_BASE')
API_VERSION = os.getenv('API_VERSION')
DEPLOYMENT_ID = os.getenv('DEPLOYMENT_ID')
TOKEN_LIMIT = int(os.getenv('TOKEN_LIMIT', 128000))

# List of code file extensions
CODE_EXTENSIONS = ['.py', '.ipynb', '.r', '.cpp', '.c', '.h', '.java', '.js', '.ts', '.html', '.css', '.scss', '.less', 
                   '.php', '.go', '.swift', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.psm1', '.bat', '.cmd', '.vbs', 
                   '.lua', '.pl', '.pm', '.tcl', '.rb', '.dart', '.kt', '.kts', '.groovy', '.scala', '.clj', '.cljs', 
                   '.cljc', '.coffee', '.elm', '.erl', '.hrl', '.ex', '.exs', '.ml', '.mli', '.mll', '.mly', '.nim', 
                   '.php3', '.php4', '.php5', '.php7', '.phps', '.phtml', '.pyc', '.pyx', '.pxd', '.pxi', '.rkt', 
                   '.rs', '.s', '.scm', '.ss', '.sml', '.sol', '.sql', '.t', '.tex', '.thy', '.v', '.vh', '.vhd', 
                   '.vim', '.vue', '.xml', '.xsd', '.xsl', '.yaml', '.yml', '.zshrc']

def get_code_files_in_dir(dir_path: str) -> List[str]:
    """Returns a list of code files in a directory."""
    code_files = []
    for root, _, files in os.walk(dir_path):
        for filename in files:
            _, ext = os.path.splitext(filename)
            if ext in CODE_EXTENSIONS:
                code_files.append(os.path.join(root, filename))
    return code_files

def read_file_content(file_path: str) -> str:
    """Reads the content of a file."""
    with open(file_path, 'r') as f:
        return f.read()

def generate_readme(api_key: str, api_base: str, api_version: str, deployment_id: str, dir_path: str, code_files: List[str]):
    """Generates a README.md file using the Azure OpenAI API."""
    openai.api_key = api_key
    openai.api_type = 'azure'
    openai.api_base = api_base
    openai.api_version = api_version

    file_contents = []
    for file_path in code_files:
        try:
            file_content = read_file_content(file_path)
            file_contents.append(file_content)
        except Exception as e:
            print(f"Failed to read file {file_path}. Error: {str(e)}")
    
    prompt = f"This directory {dir_path} contains the following code files:\n"
    for file_path, file_content in zip(code_files, file_contents):
        prompt += f"---\n"
        prompt += f"File: {file_path}\nContent:\n{file_content}\n"
        prompt += f"---\n"

    prompt += "Please provide a detailed README.md file for this repository.\n"
    prompt += "Write the README.md in markdown format.\n"
    prompt += "The beginning of the README.md file should start with the name of the repository.\n"
    prompt += "Write only the content of the generated README in the output. Nothing more.\n"
    prompt += "The README.md should have the following sections: Description, Prerequisites, Structure, Usage and Limitations.\n"
    prompt += "The Structure section should contain a detailed and comprehensive description of root folder structure, its purposes, and any relevant files in them, paying special attention to pipelines and their purpose.\n"
    prompt += "The pipelines section should be as detailed as possible, indicating description, triggers and main phases.\n"

    # Check if the number of tokens exceeds the limit
    encoding = tiktoken.encoding_for_model(deployment_id)
    tokens = encoding.encode(prompt)
    token_counts = len(tokens)

    if token_counts > TOKEN_LIMIT:
        print(f"The number of tokens in the prompt exceeds the limit ({len(tokens)}). Skipping directory {dir_path}.")
        return
    
    print(f"Generating prompt...")
    print(f"Number of prompt tokens: {token_counts}")
    print(f"Calling API...")

    try:
        response = openai.ChatCompletion.create(
            engine=deployment_id,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
    except Exception as e:
        print(f"Failed to generate README for directory {dir_path}. Error: {str(e)}")
    
    print(f"Content:")
    print(response['choices'][0]['message']['content'])

    print(f"Writing README for directory {dir_path}/README.md")

    try:
        with open(os.path.join(dir_path, 'README.md'), 'w') as f:
            f.write(response['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Failed to write README for directory {dir_path}. Error: {str(e)}")

def main(path: str):
    """Main function to run the script."""
    code_files = get_code_files_in_dir(path)
    if code_files:
        generate_readme(AZURE_OPENAI_API_KEY, API_BASE, API_VERSION, DEPLOYMENT_ID, path, code_files)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <PATH>")
        sys.exit(1)

    path = sys.argv[1]
    main(path)