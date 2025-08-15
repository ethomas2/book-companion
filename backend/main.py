from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from openai import OpenAI
from config import config
import pathlib
import os

app = FastAPI(title="Book Companion API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Validate configuration
config.validate()

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

# Load vector store ID
VECTOR_STORE_ID = None
try:
    with open("vector_store_id.txt", "r") as f:
        VECTOR_STORE_ID = f.read().strip()
    print(f"✅ Loaded vector store ID: {VECTOR_STORE_ID}")
except FileNotFoundError:
    print("⚠️  No vector store ID found. Please run rag_setup.py first.")
    VECTOR_STORE_ID = None

# Pydantic models
class BookQuery(BaseModel):
    query: str

class QuestionResponse(BaseModel):
    answer: str


@app.post("/ask")
async def ask_question(request: BookQuery):
    """
    Endpoint that sends a question about the book to OpenAI for analysis.
    Uses RAG (Retrieval-Augmented Generation) with vector store for accurate responses.
    """
    try:
        if not VECTOR_STORE_ID:
            raise HTTPException(
                status_code=500, 
                detail="RAG system not initialized. Please run rag_setup.py first."
            )

        # Use RAG with vector store
        response = client.responses.create(
            model="gpt-4o",
            input=request.query,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [VECTOR_STORE_ID],
                "max_num_results": 5
            }]
        )

        answer = response.output_text
        if not answer:
            raise HTTPException(status_code=500, detail="No answer received from OpenAI")

        return QuestionResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
