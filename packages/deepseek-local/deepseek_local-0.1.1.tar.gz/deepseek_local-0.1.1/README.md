# DeepSeek-Local

🚀 **DeepSeek-Local** is a Python package that allows you to run **DeepSeek-Coder** locally using **Ollama**. With this package, you can generate and modify code using **DeepSeek-Coder**, all without requiring an internet connection!

---

## ✨ Features
- **Offline AI Coding Assistance** – Run DeepSeek-Coder locally via Ollama.
- **Simple Installation** – Easy setup with `pip install`.
- **Seamless Integration** – Use the package in any Python project.
- **No Internet Required** – Works entirely on your local machine.

---

## 📥 Installation

### 1️⃣ Prerequisites
Ensure you have the following installed on your system:
- **Python 3.8+**
- **Ollama** ([Download Here](https://ollama.ai))

### 2️⃣ Install DeepSeek-Local
```bash
pip install deepseek-local
```

---

## 🚀 Usage

### ✅ Check if Ollama is Installed
```python
from deepseek_local.utils import is_ollama_installed

if is_ollama_installed():
    print("Ollama is installed and ready to use!")
else:
    print("Please install Ollama first.")
```

### 🔄 Install DeepSeek-Coder Model
```python
from deepseek_local import install_deepseek

install_deepseek()
```

### 🤖 Run DeepSeek-Coder
```python
from deepseek_local import run_deepseek

response = run_deepseek("Write a Python function to reverse a string.")
print(response)
```

---

## ⚡ Troubleshooting

If you encounter issues, try the following:
- Ensure **Ollama** is installed and accessible from the terminal:
  ```bash
  ollama list
  ```
- If `run_deepseek()` doesn’t return a response, verify that **DeepSeek-Coder** is installed:
  ```bash
  ollama run deepseek-coder "Test query"
  ```
- If problems persist, **restart your terminal** and ensure Python can detect Ollama.

---

## 🌍 Contributing
We welcome contributions! To contribute:
1. **Fork** this repository 🍴
2. **Create a feature branch** (`git checkout -b feature-name`)
3. **Commit your changes** (`git commit -m "Added feature XYZ"`)
4. **Push to GitHub** (`git push origin feature-name`)
5. **Submit a Pull Request** 🛠️

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 📬 Contact
Have questions or suggestions? Open an **issue** or reach out!

💻 **Email**: [saadaibani3@gmail.com]

---

⭐ If you find this project useful, **give it a star!** ⭐

