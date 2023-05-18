# README.md
## Description

This repository contains a Python script `readmefy.py` which is used to generate a `README.md` file by using the OpenAI API. It can parse code files for a given directory and generate a `README.md` file for it. Initially, the script only accepts Python files, but it can include other code files like JS, Java, C (both C and C++), C#, Go, Ruby, and PHP files.

## Prerequisites 

The `readmefy.py` script requires the following: 

- Python 3.5 or later 
- OpenAI API key
- TikTok Token library 

## Usage 

Running the script is straightforward. To run it, you can execute the command `python readmefy.py <openai_api_key>` from the command line, where `<openai_api_key>` is your OpenAI API key. After executing the script, it will generate a `README.md` file for the directory it was executed in.

## Limitations 

Due to the API token limit of 2000 tokens, the generated `README.md` file may be limited to this number of tokens. If the input code file is too long, the script will skip the directory, since it cannot generate a valid `README.md` file for it.