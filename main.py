from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import uvicorn
import lite_llm
import httpx

app = FastAPI(title="Web-based Chat Assistant")

# Allow CORS for frontend development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the LiteLLM model (assuming a default model; can be extended)
model = None

def initialize_model(model_name: str = "default") -> None:
    """
    Initialize the LiteLLM model with the specified model name.
    """
    global model
    try:
        model = lite_llm.LiteLLM(model_name)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize model: {e}")

@app.on_event("startup")
async def startup_event():
    """
    Initialize the model at startup.
    """
    initialize_model()

@app.post("/chat/")
async def chat_endpoint(
    message: str = Form(...),
    history: Optional[List[str]] = Form(None),
    model_name: Optional[str] = Form("default"),
    file: Optional[UploadFile] = File(None)
):
    """
    Handle chat requests, optionally with context file upload and conversation history.
    """
    # Re-initialize model if model_name differs
    global model
    if model_name != getattr(model, "model_name", "default"):
        try:
            initialize_model(model_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    context_text = ""
    if file:
        try:
            file_content = await file.read()
            context_text = file_content.decode("utf-8")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading uploaded file: {e}")

    # Prepare conversation history
    conversation = ""
    if history:
        conversation = "\n".join(history)

    # Combine context and conversation
    prompt = ""
    if context_text:
        prompt += f"Context:\n{context_text}\n\n"
    if conversation:
        prompt += f"Conversation History:\n{conversation}\n"
    prompt += f"User: {message}\nAssistant:"

    try:
        # Generate response from LiteLLM
        response_text = model.generate(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {e}")

    return JSONResponse(content={"response": response_text})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)