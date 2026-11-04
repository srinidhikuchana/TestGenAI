# 🧪 TestGenAI

**AI-Powered Python Unit Test Generator**

TestGenAI is a lightweight developer productivity tool that automatically generates Python unit tests using AI.

## Features
- Generate pytest unit tests from Python code
- Cover normal and edge cases
- View generated tests instantly
- Download generated test files
- Simple Streamlit interface

## Tech Stack
- Python
- Streamlit
- OpenRouter API
- Pytest

## Installation

Clone the repository:

```bash
git clone https://github.com/srinidhikuchana/TestGenAI.git
cd TestGenAI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the `OPENROUTER_API_KEY` environment variable and run:

```bash
streamlit run app.py
```

## How It Works

1. Paste a Python function into the application.
2. Click **Generate Tests**.
3. AI generates suggested pytest test cases.
4. Review and download the generated tests.
5. Run the tests locally using pytest.

## Future Improvements
- Automated test execution
- GitHub repository integration
- Test coverage reporting
- Support for multiple programming languages

## Author

**Sri Nidhi Kuchana**

[GitHub](https://github.com/srinidhikuchana) | [LinkedIn](https://www.linkedin.com/in/srinidhikuchana)

## Disclaimer

AI-generated tests should be reviewed before execution. TestGenAI does not automatically verify or execute generated tests.
