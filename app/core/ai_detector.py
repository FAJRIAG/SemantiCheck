import os
import json
import google.generativeai as genai
from app.core.processing import clean_text

# Reuse the API Key from llm.py or environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def load_ai_detector_prompt() -> str:
    path = os.path.join(os.path.dirname(__file__), "../prompts/ai_detector_prompt.txt")
    with open(path, "r") as f:
        return f.read()

def detect_ai_content(text: str) -> dict:
    """
    Analyzes text to determine if it is AI-generated.
    Returns a dict with probability, verdict, and reasoning.
    """
    if not GEMINI_API_KEY:
        return {
            "ai_probability": 0,
            "verdict": "Error",
            "reasoning": "Gemini API Key not found."
        }
    
    system_prompt = load_ai_detector_prompt()
    full_prompt = system_prompt.replace("{{TEXT}}", text)
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(full_prompt)
        
        # Clean response to ensure it's valid JSON
        result_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(result_text)
        return data
        
    except Exception as e:
        return {
            "ai_probability": 0,
            "verdict": "Error",
            "reasoning": f"Analysis failed: {str(e)}"
        }
