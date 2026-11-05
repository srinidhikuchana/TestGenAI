
import streamlit as st
import requests
import os

st.set_page_config(page_title="TestGenAI", page_icon="🧪")
st.title("TestGenAI")
st.write("Generate Python unit tests instantly using AI!")

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    api_key = st.secrets.get("OPENROUTER_API_KEY", "")

code = st.text_area("Enter Python Code", height=250)

if st.button("Generate Tests"):
    if not code.strip():
        st.warning("Please enter code!")
    elif not api_key:
        st.error("API key not configured.")
    else:
        prompt = f"""
        Generate pytest tests for the following code.
        Include normal and edge cases.
        Assume code is saved in app_code.py.
        Return only Python code without markdown.
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
                tests = tests.strip().removeprefix("```python")
                tests = tests.removeprefix("```").removesuffix("```").strip()
                st.success("Tests Generated!")
                st.code(tests, language="python")
                st.download_button(
                    "Download Tests", tests, "test_app.py"
                )
            except Exception as e:
                st.error(f"Request failed: {e}")
