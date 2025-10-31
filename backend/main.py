from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from database.database import Database
from database.init import create_database
from auth.auth import get_current_user
from models.models import (
    UserCreate, UserLogin, UserResponse, Token,
    DocumentCreate, DocumentUpdate, DocumentResponse,
    AIRequest, AIResponse, SearchQuery,
    ChatWithDocumentRequest, ChatWithDocumentResponse, ImproveWritingRequest  # New imports
)
from services.user_service import UserService
from services.document_service import DocumentService
from services.ai_service import AIService

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    print("Initializing database...")
    create_database()
    print("Database initialized successfully")
    yield
    # Shutdown: Clean up resources
    print("Shutting down...")

app = FastAPI(
    title="WPS Office Clone API",
    description="AI-powered office productivity suite backend with Gemini AI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Initialize services
ai_service = AIService()

# Health check
@app.get("/")
async def root():
    return {"message": "WPS Office Clone API with Gemini AI", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected", "ai_service": "available" if ai_service.model else "fallback"}

# ... (your existing authentication and document routes remain the same)

# AI routes
@app.post("/api/ai/process", response_model=AIResponse)
async def process_ai_request(
    request: AIRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    result = ai_service.process_ai_request(request, current_user.id)
    return result

@app.get("/api/ai/history")
async def get_ai_history(
    limit: int = 10,
    current_user: UserResponse = Depends(get_current_user)
):
    history = ai_service.get_ai_history(current_user.id, limit)
    return history

# New AI Routes for Enhanced Features
@app.post("/api/ai/chat-with-document", response_model=ChatWithDocumentResponse)
async def chat_with_document(
    request: ChatWithDocumentRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """Chat with document content using Gemini AI"""
    # If document_id is provided, fetch the document content
    document_content = request.document_content
    if not document_content and request.document_id != "chat":
        document = DocumentService.get_document_by_id(request.document_id, current_user.id)
        if document and document.content:
            # Convert document content to string for AI processing
            document_content = str(document.content)
    
    if not document_content:
        raise HTTPException(status_code=400, detail="No document content provided")
    
    result = ai_service.chat_with_document(document_content, request.question, current_user.id)
    return ChatWithDocumentResponse(**result)

@app.post("/api/ai/improve-writing")
async def improve_writing(
    request: ImproveWritingRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """Improve writing style using Gemini AI"""
    ai_request = AIRequest(
        action=AIAction.IMPROVE_WRITING,
        document_id="writing_improvement",
        parameters={"improvement_type": request.improvement_type},
        text_content=request.text
    )
    
    result = ai_service.process_ai_request(ai_request, current_user.id)
    return result

# User settings routes
@app.get("/api/user/settings")
async def get_user_settings(current_user: UserResponse = Depends(get_current_user)):
    settings = UserService.get_user_settings(current_user.id)
    return settings

@app.put("/api/user/settings")
async def update_user_settings(
    settings: dict,
    current_user: UserResponse = Depends(get_current_user)
):
    updated_settings = UserService.update_user_settings(current_user.id, settings)
    return updated_settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 8000)),
        reload=os.getenv('DEBUG', 'False').lower() == 'true'
    )