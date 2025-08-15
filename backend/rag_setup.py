#!/usr/bin/env python3
"""
RAG Setup Script for Book Companion
Uses OpenAI's Responses API with vector stores to create a searchable knowledge base
from the extracted book content.
"""

import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
from config import config

def setup_rag_system():
    """Set up the RAG system with vector store and file uploads"""

    # Initialize OpenAI client
    client = OpenAI(api_key=config.OPENAI_API_KEY) # TODO (cursor):

    print("🚀 Setting up RAG system for Book Companion...")

    # 1) Create a vector store
    print("📚 Creating vector store...")
    try:
        vs = client.vector_stores.create(name="BookCompanion-StormlightArchive")
        print(f"✅ Vector store created with ID: {vs.id}")
    except Exception as e:
        print(f"❌ Error creating vector store: {e}")
        return None

    # 2) Upload & attach files (concurrent)
    def upload_one_file(file_path: Path, vs_id: str):
        """Upload a single file and attach it to the vector store"""
        try:
            # Create file in OpenAI
            with open(file_path, "rb") as f:
                file_obj = client.files.create(file=f, purpose="assistants")

            # Attach to vector store
            client.vector_stores.files.create(vector_store_id=vs_id, file_id=file_obj.id)
            return {"filename": file_path.name, "status": "success", "file_id": file_obj.id}
        except Exception as e:
            return {"filename": file_path.name, "status": "error", "error": str(e)}

    # Get all text files from both directories
    pdf_dir = Path("pdf_extracted_pages/")
    epub_dir = Path("epub_extracted_chapters/")

    all_files = []
    if pdf_dir.exists():
        all_files.extend(pdf_dir.glob("*.txt"))
    if epub_dir.exists():
        all_files.extend(epub_dir.glob("*.txt"))

    print(f"📁 Found {len(all_files)} text files to upload")

    # Upload files concurrently
    successful_uploads = []
    failed_uploads = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(upload_one_file, p, vs.id) for p in all_files if p.exists()]

        for future in as_completed(futures):
            result = future.result()
            if result["status"] == "success":
                successful_uploads.append(result)
                print(f"✅ Uploaded: {result['filename']}")
            else:
                failed_uploads.append(result)
                print(f"❌ Failed: {result['filename']} - {result['error']}")

    print(f"\n📊 Upload Summary:")
    print(f"   ✅ Successful: {len(successful_uploads)}")
    print(f"   ❌ Failed: {len(failed_uploads)}")

    if failed_uploads:
        print("\nFailed uploads:")
        for fail in failed_uploads:
            print(f"  - {fail['filename']}: {fail['error']}")

    # 3) Test the RAG system
    print("\n🧪 Testing RAG system...")
    try:
        # Test search
        search_query = "Cenn character"
        print(f"🔍 Testing search for: '{search_query}'")

        search_results = client.vector_stores.search(
            vector_store_id=vs.id,
            query=search_query
        )

        print(f"📖 Found {len(search_results.data)} results:")
        for i, hit in enumerate(search_results.data[:3]):
            print(f"  {i+1}. {hit.filename} (score: {hit.score:.3f})")

        # Test RAG query
        print(f"\n🤖 Testing RAG query...")
        rag_response = client.responses.create(
            model="gpt-4o",
            input="Who is Cenn and what role does he play in the Stormlight Archive?",
            tools=[{
                "type": "file_search",
                "vector_store_ids": [vs.id],
                "max_num_results": 5
            }]
        )

        print("\n=== RAG Answer ===")
        print(rag_response.output_text)

        # Show retrieved sources
        print("\n=== Retrieved Sources ===")
        print("📄 File search results included in response")
        print(f"Response object type: {type(rag_response)}")
        print(f"Available attributes: {dir(rag_response)}")

        print("\n🎉 RAG system is working!")
        return vs.id

    except Exception as e:
        print(f"❌ Error testing RAG system: {e}")
        return None

def query_rag(question: str, vector_store_id: str):
    """Query the RAG system with a question"""
    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)

        response = client.responses.create(
            model="gpt-4o",
            input=question,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [vector_store_id],
                "max_num_results": 5
            }]
        )

        return {
            "answer": response.output_text,
            "sources": []
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Set up the RAG system
    vector_store_id = setup_rag_system()

    if vector_store_id:
        print(f"\n💾 Vector Store ID: {vector_store_id}")
        print("💡 You can now use this ID in your main.py to query the RAG system!")

        # Save the vector store ID for later use
        with open("vector_store_id.txt", "w") as f:
            f.write(vector_store_id)
        print("💾 Vector store ID saved to vector_store_id.txt")
    else:
        print("❌ Failed to set up RAG system")
