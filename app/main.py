from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
import uvicorn
import os

from app.core.embedding import get_model_instance
from app.core.processing import preprocess_for_embedding
from app.core.similarity import calculate_similarity, get_risk_level
from app.core.llm import analyze_with_llm
from app.core.ai_detector import detect_ai_content

# Lifespan context to load model on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    get_model_instance()
    yield
    # Clean up (if needed)

app = FastAPI(title="SemantiCheck API", version="1.0", lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('app/static/index.html')

class TextRequest(BaseModel):
    text_a: str
    text_b: str

class SingleTextRequest(BaseModel):
    text: str

class SimilarityResponse(BaseModel):
    similarity_score: float
    risk_level: str
    message: str

class DetailedResponse(BaseModel):
    similarity_score: float
    risk_level: str
    detailed_analysis: str

class AIDetectionResponse(BaseModel):
    ai_probability: int
    verdict: str
    reasoning: str

@app.post("/analyze/local", response_model=SimilarityResponse)
async def analyze_local(request: TextRequest):
    """
    Fast, local analysis using Sentence Transformers.
    """
    if not request.text_a or not request.text_b:
        raise HTTPException(status_code=400, detail="Both texts must be provided.")

    # Preprocess
    clean_a = preprocess_for_embedding(request.text_a)
    clean_b = preprocess_for_embedding(request.text_b)

    # Embed
    model = get_model_instance()
    emb_a = model.get_embedding(clean_a)
    emb_b = model.get_embedding(clean_b)

    # Calculate Similarity
    score = calculate_similarity(emb_a, emb_b)
    risk = get_risk_level(score)

    return SimilarityResponse(
        similarity_score=round(score, 4),
        risk_level=risk,
        message="Local analysis complete."
    )

@app.post("/analyze/detailed", response_model=DetailedResponse)
async def analyze_detailed(request: TextRequest):
    """
    Detailed analysis using LLM (Gemini).
    Includes local scoring as well.
    """
    if not request.text_a or not request.text_b:
        raise HTTPException(status_code=400, detail="Both texts must be provided.")

    # Local Score first
    clean_a = preprocess_for_embedding(request.text_a)
    clean_b = preprocess_for_embedding(request.text_b)
    
    model = get_model_instance()
    emb_a = model.get_embedding(clean_a)
    emb_b = model.get_embedding(clean_b)
    
    score = calculate_similarity(emb_a, emb_b)
    risk = get_risk_level(score)

    # LLM Analysis
    analysis_text = analyze_with_llm(request.text_a, request.text_b)

    return DetailedResponse(
        similarity_score=round(score, 4),
        risk_level=risk,
        detailed_analysis=analysis_text
    )

@app.post("/detect-ai", response_model=AIDetectionResponse)
async def detect_ai(request: SingleTextRequest):
    """
    Detects if text is AI-generated.
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Text must be provided.")
    
    result = detect_ai_content(request.text)
    return AIDetectionResponse(**result)

@app.post("/detect-ai/file", response_model=AIDetectionResponse)
async def detect_ai_file(file: UploadFile = File(...)):
    """
    Detects if uploaded file (.txt, .docx) content is AI-generated.
    """
    try:
        from app.core.processing import extract_text_from_file
        text = await extract_text_from_file(file)
        
        if not text:
             raise HTTPException(status_code=400, detail="Could not extract text from file.")

        result = detect_ai_content(text)
        return AIDetectionResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
