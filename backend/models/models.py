from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class DocumentType(str, Enum):
    WRITER = "writer"
    SPREADSHEET = "spreadsheet"
    PRESENTATION = "presentation"
    PDF = "pdf"

class PermissionLevel(str, Enum):
    VIEW = "view"
    COMMENT = "comment"
    EDIT = "edit"

class AIAction(str, Enum):
    SUMMARIZE = "summarize"
    GRAMMAR_CHECK = "grammar_check"
    TRANSLATE = "translate"
    ANALYZE_DATA = "analyze_data"
    FORMAT = "format"
    GENERATE_CONTENT = "generate_content"

# User Models
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Document Models
class DocumentBase(BaseModel):
    title: str
    document_type: DocumentType

class DocumentCreate(DocumentBase):
    content: Optional[Dict[str, Any]] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    version: Optional[int] = None

class DocumentResponse(DocumentBase):
    id: str
    user_id: str
    content: Optional[Dict[str, Any]] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Collaboration Models
class CollaboratorBase(BaseModel):
    user_id: str
    permission_level: PermissionLevel

class CollaboratorCreate(CollaboratorBase):
    document_id: str

class CollaboratorResponse(CollaboratorBase):
    id: str
    invited_at: datetime
    user_name: str
    user_email: str

    class Config:
        from_attributes = True

# AI Models
class AIRequest(BaseModel):
    action: AIAction
    document_id: str
    parameters: Optional[Dict[str, Any]] = None
    text_content: Optional[str] = None

class AIResponse(BaseModel):
    id: str
    action: AIAction
    input_data: Optional[Dict[str, Any]] = None
    output_data: Dict[str, Any]
    processing_time_ms: int
    created_at: datetime

    class Config:
        from_attributes = True

# Authentication Models
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    user_id: Optional[str] = None

# Search Models
class SearchQuery(BaseModel):
    query: str
    document_type: Optional[DocumentType] = None
    limit: int = 20
    offset: int = 0

class SearchResponse(BaseModel):
    results: List[DocumentResponse]
    total: int
    has_more: bool