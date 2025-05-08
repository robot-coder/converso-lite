# README.md

# Web-based Chat Assistant with FastAPI and LiteLLM

This project implements a web-based conversational AI assistant using a front-end JavaScript interface and a back-end Python FastAPI server. The server interacts with LiteLLM to provide AI-powered responses, supporting features such as model selection, conversation history, and optional file uploads for context and multimodal responses.

## Features

- Select different language models supported by LiteLLM
- Maintain conversation history for context-aware responses
- Upload files (images, documents) to provide additional context
- Multimodal responses (text and images)
- Modular and well-structured codebase with error handling

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- LiteLLM
- python-multipart
- Starlette
- httpx

## Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

## Usage

Use the front-end interface (not included in this repo) to interact with the assistant. The backend API provides endpoints for sending messages, uploading files, and retrieving conversation history.

## API Endpoints

- `POST /chat/`  
  Send a message to the assistant. Supports optional file uploads for context.

- `GET /history/`  
  Retrieve conversation history.

## Code Structure

- `main.py`: Main FastAPI application with route handlers
- `requirements.txt`: Dependencies list

---

# main.py

```python
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Optional
import httpx
import asyncio
import os

# Assuming LiteLLM is a hypothetical library; replace with actual implementation
# from lite_llm import LiteLLM

app = FastAPI()

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Placeholder for LiteLLM model instance
class LiteLLM:
    def __init__(self, model_name: str):
        self.model_name = model_name

    async def generate_response(self, prompt: str, context_files: Optional[List[bytes]] = None) -> str:
        # Placeholder implementation
        # Replace with actual LiteLLM interaction
        return f"Echo: {prompt}"

# Initialize with default model
model_instance = LiteLLM("default-model")

# Store conversation history in-memory (for demo purposes)
conversation_history: List[dict] = []

@app.post("/chat/")
async def chat_endpoint(
    message: str = Form(...),
    model_name: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None)
):
    """
    Handle chat messages, optional model selection, and file uploads for context.
    """
    try:
        # Update model if specified
        if model_name:
            global model_instance
            model_instance = LiteLLM(model_name)

        # Read uploaded files if any
        context_files = []
        if files:
            for file in files:
                content = await file.read()
                context_files.append(content)

        # Generate response from LiteLLM
        response_text = await model_instance.generate_response(message, context_files)

        # Save to conversation history
        conversation_entry = {
            "user": message,
            "assistant": response_text
        }
        conversation_history.append(conversation_entry)

        return JSONResponse(content={
            "response": response_text,
            "history": conversation_history
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/")
async def get_history():
    """
    Retrieve the conversation history.
    """
    return JSONResponse(content={"history": conversation_history})

# Entry point for running the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

# requirements.txt

```
fastapi
uvicorn
lite_llm
python-multipart
starlette
httpx
```