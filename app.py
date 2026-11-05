import streamlit as st
import requests
import os
from urllib.parse import urlparse, quote

st.set_page_config(page_title="TestGenAI", page_icon="🧪")
st.title("TestGenAI")
st.write("Generate unit tests using AI — from code or GitHub!")

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    api_key = st.secrets.get("OPENROUTER_API_KEY", "")

frameworks = {
    "Python": ("pytest", ".py", "test_app.py"),
    "Java": ("JUnit 5", ".java", "GeneratedTest.java"),
    "JavaScript": ("Jest", ".js", "app.test.js"),
    "TypeScript": ("Vitest", ".ts", "app.test.ts"),
    "C": ("Unity", ".c", "test_app.c"),
    "C++": ("Google Test", ".cpp", "test_app.cpp")
}

language=st.selectbox("Select Language", list(frameworks))
framework, extension, filename = frameworks[language]
method = st.radio("Input Method", ["Paste Code", "GitHub Repository"])

code = ""
source_file="app_code"+extension

if method=="Paste Code":
    code=st.text_area("Enter Your Code", height=250)

else:
    repo_url=st.text_input(
        "Public GitHub Repository URL",
        placeholder="https://github.com/username/repository"
    )

    if repo_url:
        try:
            parsed = urlparse(repo_url.strip())
            parts = parsed.path.strip("/").split("/")

            if parsed.scheme != "https" or parsed.netloc.lower() not in (
                "github.com", "www.github.com"
            ) or len(parts) != 2 or not all(parts):
                st.error("Enter a valid GitHub repository URL.")
            else:
                owner, repo = parts
                repo = repo.removesuffix(".git")
                base = f"https://api.github.com/repos/{owner}/{repo}"

                info = requests.get(base, timeout=15)
                info.raise_for_status()
                branch = info.json()["default_branch"]

                tree = requests.get(
                    f"{base}/git/trees/{quote(branch, safe='')}?recursive=1",
                    timeout=20
                )
                tree.raise_for_status()
                tree_data = tree.json()

                if tree_data.get("truncated"):
                    st.warning("Large repository: some files may be missing.")

                files = [
                    item["path"] for item in tree_data["tree"]
                    if item["type"] == "blob"
                    and item["path"].endswith(extension)
                ]

                if files:
                    selected = st.selectbox("Select Source File", files)
                    source_file = selected

                    raw = requests.get(
                        f"https://raw.githubusercontent.com/"
                        f"{owner}/{repo}/{quote(branch, safe='')}/"
                        f"{quote(selected, safe='/')}",
                        timeout=20
                    )
                    raw.raise_for_status()

                    if len(raw.content) > 100_000:
                        st.error("File too large. Choose a smaller file.")
                    else:
                        code = raw.text
                        st.code(code, language=language.lower())
                else:
                    st.warning(f"No {language} source files found.")

        except requests.RequestException as e:
            st.error(f"GitHub request failed: {e}")
        except (KeyError, ValueError):
            st.error("Could not read repository information.")
if st.button("Generate Tests"):
    if not code.strip():
        st.warning("Please provide source code first!")
    elif not api_key:
        st.error("OpenRouter API key not configured.")
    else:
        prompt = f"""
Generate {framework} unit tests for this {language} code.
Include normal, edge, and error cases where appropriate.
The source file is named: {source_file}
Include correct imports based on that filename.
Return only test code without markdown.
Source code:
{code}
"""
        with st.spinner("Generating tests..."):
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
                tests = res.json()["choices"][0]["message"]["content"].strip()

                if tests.startswith("```"):
                    tests = tests.split("\n", 1)[-1]
                    tests = tests.removesuffix("```").strip()

                st.success("Tests Generated!")
                st.code(tests, language=language.lower())
                st.download_button("Download Tests", tests, filename)

            except (requests.RequestException, KeyError, IndexError, TypeError) as e:
                st.error(f"Generation failed: {e}")
