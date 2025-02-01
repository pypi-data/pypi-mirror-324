import subprocess

def is_ollama_installed():
    """Check if Ollama is installed."""
    try:
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def install_ollama():
    """Guide users to install Ollama if not found."""
    print("Ollama is not installed. Please install it from https://ollama.ai")
