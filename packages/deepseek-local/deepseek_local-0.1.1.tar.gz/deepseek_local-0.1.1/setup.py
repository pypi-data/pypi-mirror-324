from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="deepseek_local",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["ollama"],
    entry_points={
        "console_scripts": [
            "deepseek-install=deepseek_local.deepseek:install_deepseek",
            "deepseek-run=deepseek_local.deepseek:run_deepseek",
        ]
    },
    author="Saad Aibani",
    author_email="saadaibani3@gmail.com",
    description="A Python library for running DeepSeek-Coder locally using Ollama.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandbox259/deepseek_local",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
