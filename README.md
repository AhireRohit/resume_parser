# 💼 LLM-Powered Resume Screener

A smart, locally-hosted ATS-style tool that uses **open-source LLMs** (like Mistral or Phi) to analyze resumes against job descriptions. Built with Python, Gradio, and Ollama — this AI screener parses resume PDFs, compares them with job descriptions, and gives match scores, strengths, weaknesses, and interview suggestions.
---

## 🚀 Features

- 🧠 Uses **locally hosted LLMs** (no OpenAI API keys needed)
- 📄 Upload **any PDF resume** — even with messy layouts
- 📝 Paste **any job description** — tech, business, etc.
- ⚙️ Extracts structured resume info (name, skills, experience)
- 🎯 Analyzes candidate fit vs JD and returns:
  - ✅ Match score (0–10)
  - 🟢 Strengths
  - 🔴 Weaknesses
  - ❓ Suggested interview questions
- 📊 Clean, responsive **Gradio UI**
- ⏱️ Shows time taken for full LLM evaluation
- 💻 100% private, offline, and free to run

---

## 📷 Demo Screenshot

![image](https://github.com/user-attachments/assets/f53efe8c-c56f-4d2e-913e-82a7fbf39d8c)

---

## 🛠️ Tech Stack

| Component        | Tech                              |
|------------------|-----------------------------------|
| LLM Backend      | [Ollama](https://ollama.com) + Mistral / Phi |
| Interface        | [Gradio](https://gradio.app)      |
| PDF Parsing      | PyMuPDF (`fitz`)                  |
| Prompting        | Prompt engineering + JSON parsing |
| Hosting          | Local, or Hugging Face (UI only)  |

---

## 📦 Installation

### 🔧 Requirements
- Python 3.8+
- GPU (optional but recommended — at least 4GB VRAM)
- [Ollama](https://ollama.com/) installed (to run models like `mistral`, `phi`, or `gemma`)

### ✅ Install dependencies:
```bash
pip install -r requirements.txt
```
Example requirements.txt:
```bash
gradio
requests
PyMuPDF
```
💻 How to Run Locally
1. Start your model with Ollama
```bash

ollama pull mistral
ollama run mistral
```
Or use a lighter model:

```bash
ollama pull phi
ollama run phi
```
2. Run the app
```bash
python main.py
```
