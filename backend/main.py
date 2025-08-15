from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from openai import OpenAI
from config import config
import pathlib

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

# Pydantic models
class BookQuery(BaseModel):
    query: str

class QuestionResponse(BaseModel):
    answer: str

def get_book_context(num_pages: int = 50) -> str:
    """
    Get the first couple of chapters of the book as context.
    Returns a string with the combined text of the first N chapters.
    """
    try:
        # Get the first N chapter files using pathlib
        chapters_dir = pathlib.Path("pdf_extracted_pages/")
        pages = sorted(chapters_dir.glob("page_*.txt"))[:num_pages] # TODO (cursor): read all pages in and sort numerically instead of lexiographically. (Use regex to extract the number from the filename)

        context_parts = []
        for page in pages:

            content = page.read_text(encoding='utf-8').strip()
            if content:
                # Extract chapter number from filename
                chapter_num = page.stem.split('_')[-1] # TODO: use regex to extract the number from the filename
                context_parts.append(f"Chapter {chapter_num}:\n{content}\n")


        return "\n".join(context_parts) if context_parts else "No book context available."

    except Exception as e:
        print(f"Error getting book context: {e}")
        return "Error retrieving book context."


@app.post("/ask")
async def ask_question(request: BookQuery):
    """
    Endpoint that sends a question about the book to OpenAI for analysis.
    Automatically includes relevant book context from disk for more accurate responses.
    """
    try:
        # Always get book context automatically
        book_context = get_book_context()

        # Create a comprehensive prompt with book context
        prompt = f"""
        Read the following book content and answer the question based on the content. ONLY answer based on the book content.

        Question: {request.query}

        ---

        Context: {book_context}
        """

        response = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful book companion assistant that provides accurate answers based on the provided book content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0
        )

        answer = response.choices[0].message.content

        return QuestionResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
