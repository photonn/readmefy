import os
import openai
from typing import List
import sys
import tiktoken

# List of code file extensions
CODE_EXTENSIONS = ['.py', '.ipynb', '.r', '.cpp', '.c', '.h', '.java', '.js', '.ts', '.html', '.css', '.scss', '.less', '.php', '.go', '.swift', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.psm1', '.bat', '.cmd', '.vbs', '.lua', '.pl', '.pm', '.tcl', '.rb', '.dart', '.kt', '.kts', '.groovy', '.scala', '.clj', '.cljs', '.cljc', '.coffee', '.elm', '.erl', '.hrl', '.ex', '.exs', '.ml', '.mli', '.mll', '.mly', '.nim', '.php3', '.php4', '.php5', '.php7', '.phps', '.phtml', '.pyc', '.pyx', '.pxd', '.pxi', '.rkt', '.rs', '.s', '.scm', '.ss', '.sml', '.sol', '.sql', '.t', '.tex', '.thy', '.v', '.vh', '.vhd', '.vim', '.vue', '.xml', '.xsd', '.xsl', '.yaml', '.yml', '.zshrc']
TOKEN_LIMIT = 2000
MODEL = "text-davinci-003"

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

def generate_readme(api_key: str, dir_path: str, code_files: List[str]):
    """Generates a README.md file using the OpenAI API."""
    openai.api_key = api_key
    file_contents = []
    for file_path in code_files:
        try:
            file_content = read_file_content(file_path)
            file_contents.append(file_content)
        except Exception as e:
            print(f"Failed to read file {file_path}. Error: {str(e)}")
    prompt = f"This directory {dir_path} contains the following code files:\n"
    for file_path, file_content in zip(code_files, file_contents):
        prompt += f"File: {file_path}\nContent:\n{file_content}\n"

    prompt += "Please provide a detailed README.md file for this repository.\n"
    prompt += "Write the README.md in markdown format.\n"
    prompt += "The README.md should have the following sections: Description, Prerequisites (python version, imports, and keys), Usage and Limitations.\n"

    # Check if the number of tokens exceeds the limit
    encoding = tiktoken.encoding_for_model(MODEL)
    tokens = encoding.encode(prompt)
    token_counts = 0
    for token in tokens:
        token_counts += 1

    if token_counts > TOKEN_LIMIT:  # Here, 500 is the token limit.
        print(f"The number of tokens in the prompt exceeds the limit. Skipping directory {dir_path}.")
        return
    
    print(f"Generating prompt...")
    print(f"Number of prompt tokens: {token_counts}")

    try:
        response = openai.Completion.create(
            engine=MODEL,
            prompt=prompt,
            max_tokens=TOKEN_LIMIT
        )

        with open(os.path.join(dir_path, 'README.md'), 'w') as f:
            f.write(response.choices[0].text.strip())
    except Exception as e:
        print(f"Failed to generate README for directory {dir_path}. Error: {str(e)}")


def main(api_key: str):
    """Main function to run the script."""
    for root, dirs, files in os.walk('.'):
        if files:
            code_files = get_code_files_in_dir(root)
            if code_files:
                generate_readme(api_key, root, code_files)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <openai_api_key>")
        sys.exit(1)

    openai_api_key = sys.argv[1]
    main(openai_api_key)
