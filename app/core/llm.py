import os
from dotenv import load_dotenv
import google.generativeai as genai
from app.core.processing import clean_text

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
# Expects GEMINI_API_KEY to be set in environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def load_system_prompt() -> str:
    """
    Loads the system prompt from the prompts directory.
    """
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/system_prompt.txt")
    with open(prompt_path, "r") as f:
        return f.read()

def analyze_with_llm(text_a: str, text_b: str) -> str:
    """
    Sends Text A and Text B to the LLM for detailed analysis.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not found in environment variables. detailed analysis unavailable."

    system_prompt = load_system_prompt()
    
    # Construct the user prompt
    user_prompt = f"""
Text A:
\"\"\"{text_a}\"\"\"

Text B:
\"\"\"{text_b}\"\"\"
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        # Combining system prompt and user prompt effectively
        # Gemini Python SDK doesn't always have a distinct 'system' role in `generate_content` the same way OpenAI does, 
        # but usage usually implies prepending instructions.
        # Alternatively, use system_instruction if supported by the model version.
        
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error during LLM analysis: {str(e)}"
