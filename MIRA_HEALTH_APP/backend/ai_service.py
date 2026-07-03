import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_prediction(full_name, glucose, haemoglobin, cholesterol):
    prompt = f"""You are a health prediction assistant.
Based on these blood test results, give a concise 2-3 sentence health risk prediction.
Use plain English. No bullet points, no markdown.

Patient: {full_name}
Glucose:      {glucose} mg/dL    (normal fasting: 70–100)
Haemoglobin:  {haemoglobin} g/dL (normal: 12–17)
Cholesterol:  {cholesterol} mg/dL (normal: below 200)
"""
    models = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-flash-latest"]
    for m in models:
        try:
            model = genai.GenerativeModel(m)
            resp  = model.generate_content(prompt)
            text  = resp.text.strip()
            if text:
                return text
        except Exception as e:
            print(f"[ai_service] model '{m}' failed: {e}")
            continue
    return "AI prediction unavailable. Please review blood values manually."