import subprocess
import ollama
from .utils import is_ollama_installed, install_ollama

def install_deepseek():
    """Pull the DeepSeek-Coder model using Ollama."""
    if not is_ollama_installed():
        install_ollama()
        return

    try:
        print("Downloading DeepSeek-Coder model...")
        subprocess.run(["ollama", "pull", "deepseek-coder"], check=True)
        print("DeepSeek-Coder installed successfully.")
    except subprocess.CalledProcessError:
        print("Error installing DeepSeek-Coder. Make sure Ollama is correctly installed.")

def run_deepseek(prompt):
    """Run inference on DeepSeek-Coder."""
    if not is_ollama_installed():
        install_ollama()
        return

    try:
        response = ollama.chat(model="deepseek-coder", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error running DeepSeek-Coder: {e}"
