import fitz  # PyMuPDF
import requests
import json
import gradio as gr
import time

# --- Step 1: Extract text from resume PDF ---
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

# --- Step 2: Prompt to parse resume into structured JSON ---
def build_resume_parsing_prompt(raw_resume_text):
    return f"""
You are an expert resume parser. Extract the following fields from the given resume:

- Name
- Total years of professional experience (estimate if not directly given)
- Skills (as a list)
- Work History (list of previous jobs, companies, duration, and roles)
- Education (degree, college, year)

Respond in this JSON format:
{{
  "name": "...",
  "experience_years": ...,
  "skills": ["...", "..."],
  "work_history": [...],
  "education": [...]
}}

Resume:
{raw_resume_text}
"""

# --- Step 3: Prompt to compare resume and job description ---
def build_matching_prompt(parsed_resume_json, job_description):
    return f"""
You are an expert HR analyst.

Given the candidate's resume (structured JSON) and a job description, analyze the match:

1. Rate the candidate's fit from 0–10
2. List 3 strengths and 3 weaknesses
3. Suggest 3 interview questions

Resume JSON:
{parsed_resume_json}

Job Description:
{job_description}
"""

# --- Step 4: Call local LLM (Ollama) with the prompt ---
def call_llm_with_prompt(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt},
        stream=True
    )
    result = ""
    for line in response.iter_lines():
        if line:
            json_line = json.loads(line)
            result += json_line.get("response", "")
    return result

# --- Step 5: Parse resume and evaluate match ---
def parse_resume_with_llm(pdf_path):
    resume_text = extract_text_from_pdf(pdf_path)
    prompt = build_resume_parsing_prompt(resume_text)
    parsed_resume_json = call_llm_with_prompt(prompt)
    return parsed_resume_json

def evaluate_resume_against_jd(parsed_resume_json, job_description):
    prompt = build_matching_prompt(parsed_resume_json, job_description)
    return call_llm_with_prompt(prompt)

# --- Step 6: Gradio Interface ---
def ats_screening_ui(pdf_file, job_description):
    start_time = time.time()
    parsed_resume = parse_resume_with_llm(pdf_file.name)
    match_result = evaluate_resume_against_jd(parsed_resume, job_description)
    elapsed_time = time.time() - start_time

    output_markdown = f"""
### 📄 Parsed Resume

**Name**: {json.loads(parsed_resume).get('name', 'N/A')}  
**Experience**: {json.loads(parsed_resume).get('experience_years', 'N/A')} years  
**Skills**: {', '.join(json.loads(parsed_resume).get('skills', []))}

---

### 📊 Match Evaluation
{match_result.strip()}
"""
    return gr.update(value=output_markdown), f"⏱️ Time taken: {elapsed_time:.2f} seconds"

if __name__ == "__main__":
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="orange")) as demo:
        gr.Markdown("# 💼 LLM-Powered Resume Screener")
        gr.Markdown("Upload a resume and paste a job description to evaluate the match using a locally hosted Mistral model.")

        with gr.Row():
            with gr.Column():
                resume_input = gr.File(label="📄 Upload Resume (PDF)")
                jd_input = gr.Textbox(label="📝 Paste Job Description", lines=10, placeholder="Paste the job description here...")
                submit_btn = gr.Button("🔍 Submit", variant="primary")
            with gr.Column():
                output_box = gr.Markdown("", label="📊 Output")
                time_box = gr.Textbox(label="⏱️ Processing Time", interactive=False)

        submit_btn.click(fn=ats_screening_ui, inputs=[resume_input, jd_input], outputs=[output_box, time_box])

    demo.launch(share=True)
