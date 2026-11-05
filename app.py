import streamlit as st
import requests
import os

st.set_page_config(page_title="TestGenAI", page_icon="🧪")
st.title("TestGenAI")
st.write("Generate unit tests for multiple languages using AI!")

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    api_key = st.secrets.get("OPENROUTER_API_KEY", "")

frameworks = {
    "Python": ("pytest", "test_app.py"),
    "Java": ("JUnit 5", "GeneratedTest.java"),
    "JavaScript": ("Jest", "app.test.js"),
    "TypeScript": ("Vitest", "app.test.ts"),
    "C": ("Unity", "test_app.c"),
    "C++": ("Google Test", "test_app.cpp")
}

language = st.selectbox("Select Language", list(frameworks.keys()))
framework, filename = frameworks[language]
code = st.text_area(f"Enter {language} Code", height=250)
if st.button("Generate Tests"):
    if not code.strip():
        st.warning("Please enter code!")
    elif not api_key:
        st.error("API key not configured.")
    else:
        prompt = f"""
        Generate unit tests for this {language} code.
        Use the {framework} testing framework.
        Include normal, edge, and error cases where appropriate.
        Include necessary imports and assume the source code
        is in a separate file.
        Return only executable test code, without markdown.

        Code:
        {code}
        """
        with st.spinner("Generating..."):
            try:
                res = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "openrouter/free",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ]
                    },
                    timeout=60
                )
                res.raise_for_status()
                tests = res.json()["choices"][0]["message"]["content"]
                tests = tests.strip()
                if tests.startswith("```"):
                    tests = tests.split("\n", 1)[-1]
                    tests = tests.removesuffix("```").strip()

                st.success("Tests Generated!")
                st.code(tests, language=language.lower())
                st.download_button(
                    "Download Tests", tests, filename
                )
            except Exception as e:
                st.error(f"Request failed: {e}")
