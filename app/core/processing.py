import re
from io import BytesIO
from fastapi import UploadFile
import docx

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing excessive whitespace and stripping.
    """
    if not text:
        return ""
    # Remove excessive newlines and spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_for_embedding(text: str) -> str:
    """
    Prepares text for embedding. 
    Currently just cleans it, but can be extended.
    """
    return clean_text(text)

async def extract_text_from_file(file: UploadFile) -> str:
    """
    Extracts text from an uploaded file (.txt or .docx).
    """
    content = await file.read()
    
    if file.filename.endswith(".txt"):
        try:
            return clean_text(content.decode("utf-8"))
        except UnicodeDecodeError:
            # Fallback for other encodings if needed, or raise error
            return clean_text(content.decode("latin-1"))
            
    elif file.filename.endswith(".docx"):
        doc = docx.Document(BytesIO(content))
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return clean_text("\n".join(full_text))
    
    else:
        raise ValueError("Unsupported file format. Please upload .txt or .docx")
