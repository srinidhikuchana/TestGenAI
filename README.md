# TestGenAI

TestGenAI is a small project I built to make writing unit tests a little easier.

While working on Python projects, I noticed that writing test cases for every function can get repetitive. So I wanted to try building a tool that could generate basic test cases automatically.

The app takes Python code as input and uses the OpenRouter API to generate pytest test cases.

## What it does

- Takes Python code as input
- Generates unit tests using AI
- Includes normal and edge cases
- Lets users download the generated tests as a Python file

## Tech Stack

- Python
- Streamlit
- OpenRouter API
- Pytest

## Running locally

Clone the repository:

```bash
git clone https://github.com/srinidhikuchana/TestGenAI.git
cd TestGenAI
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Set your OpenRouter API key as an environment variable named `OPENROUTER_API_KEY`.

Start the application:

```bash
streamlit run app.py
```

## How to use

1. Paste a Python function into the text area.
2. Click **Generate Tests**.
3. Wait for the generated test cases.
4. Review the tests and download the file if needed.

The generated tests can be run locally using pytest. They may need some changes depending on the code, since AI-generated tests aren't always correct.

## What I learned

This project helped me practice working with APIs, handling responses, and building a simple interface with Streamlit.

I also got to explore how AI can be used for small developer tools instead of just chat applications.

## Things I'd like to add

- Support for more programming languages
- An option to run tests directly
- Test coverage information
- GitHub repository integration

## Author

Sri Nidhi Kuchana

[GitHub](https://github.com/srinidhikuchana) | [LinkedIn](https://www.linkedin.com/in/srinidhikuchana)
