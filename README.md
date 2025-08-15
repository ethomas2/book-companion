# Book Companion

A React + FastAPI application for asking questions about books using AI.

## Features

- **Frontend**: React TypeScript app with react-query for API calls
- **Backend**: FastAPI stub ready for OpenAI integration
- **Book Extraction**: Scripts to extract text from EPUB and PDF files
- **Q&A Interface**: Clean UI for asking questions about books

## Quick Start

### 1. Start the Backend

```bash
cd backend
source ../venv/bin/activate  # If using virtual environment
pip install -r requirements.txt
python main.py
```

The backend will start on http://localhost:8000

### 2. Start the Frontend

```bash
cd frontend
npm install
npm start
```

The frontend will start on http://localhost:3000

### 3. Test the Application

- Open http://localhost:3000 in your browser
- Type a question about "The Way of Kings"
- The backend will return a stub response (ready for OpenAI integration)

## Project Structure

```
book-companion/
├── backend/
│   ├── main.py                    # FastAPI server
│   ├── extract_epub.py            # EPUB text extraction
│   ├── extract_pdf.py             # PDF text extraction
│   ├── requirements.txt            # Python dependencies
│   ├── epub_extracted_chapters/   # Extracted EPUB chapters
│   └── pdf_extracted_pages/       # Extracted PDF pages
├── frontend/
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── hooks/                 # Custom hooks
│   │   ├── api/                   # API client
│   │   └── types/                 # TypeScript types
│   └── package.json               # Node dependencies
└── README.md                      # This file
```

## Current Status

- ✅ **Frontend**: React TypeScript app with react-query
- ✅ **Backend**: FastAPI stub with CORS enabled
- ✅ **Book Extraction**: EPUB and PDF text extraction scripts
- 🔄 **Next Step**: Integrate OpenAI API to send book text + questions

## Development

### Backend Development
- FastAPI with automatic API documentation at http://localhost:8000/docs
- CORS enabled for frontend development
- Ready for OpenAI integration

### Frontend Development
- React 19 with TypeScript
- react-query for API state management
- Inline styles (no external CSS framework)
- Responsive design

## Next Steps

1. **OpenAI Integration**: Modify backend to send book text with questions
2. **Text Chunking**: Break large books into manageable pieces
3. **RAG Implementation**: Add vector search for better performance
4. **User Experience**: Add question history, bookmarks, etc.
