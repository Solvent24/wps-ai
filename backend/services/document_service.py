import uuid
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from database.database import Database
from models.models import DocumentCreate, DocumentUpdate, DocumentResponse, DocumentType

class DocumentService:
    @staticmethod
    def create_document(document: DocumentCreate, user_id: str) -> DocumentResponse:
        """Create new document"""
        document_id = str(uuid.uuid4())
        
        content_json = json.dumps(document.content) if document.content else None
        
        Database.execute_query(
            """
            INSERT INTO documents (id, user_id, title, document_type, content)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (document_id, user_id, document.title, document.document_type, content_json)
        )
        
        return DocumentService.get_document_by_id(document_id, user_id)
    
    @staticmethod
    def get_document_by_id(document_id: str, user_id: str) -> Optional[DocumentResponse]:
        """Get document by ID with access check"""
        document_data = Database.execute_single_query(
            """
            SELECT d.* FROM documents d 
            WHERE d.id = %s AND d.user_id = %s
            """,
            (document_id, user_id)
        )
        
        if not document_data:
            return None
        
        return DocumentService._map_document_response(document_data)
    
    @staticmethod
    def get_user_documents(user_id: str, document_type: Optional[DocumentType] = None) -> List[DocumentResponse]:
        """Get all documents for user"""
        if document_type:
            documents_data = Database.execute_query(
                "SELECT * FROM documents WHERE user_id = %s AND document_type = %s ORDER BY updated_at DESC",
                (user_id, document_type),
                fetch=True
            )
        else:
            documents_data = Database.execute_query(
                "SELECT * FROM documents WHERE user_id = %s ORDER BY updated_at DESC",
                (user_id,),
                fetch=True
            )
        
        return [DocumentService._map_document_response(doc) for doc in documents_data]
    
    @staticmethod
    def update_document(document_id: str, user_id: str, updates: DocumentUpdate) -> Optional[DocumentResponse]:
        """Update document"""
        document = DocumentService.get_document_by_id(document_id, user_id)
        if not document:
            return None
        
        update_fields = []
        params = []
        
        if updates.title is not None:
            update_fields.append("title = %s")
            params.append(updates.title)
        
        if updates.content is not None:
            content_json = json.dumps(updates.content)
            update_fields.append("content = %s")
            params.append(content_json)
        
        if not update_fields:
            return document
        
        update_fields.append("updated_at = %s")
        params.append(datetime.now())
        params.append(document_id)
        
        query = f"UPDATE documents SET {', '.join(update_fields)} WHERE id = %s"
        Database.execute_query(query, params)
        
        return DocumentService.get_document_by_id(document_id, user_id)
    
    @staticmethod
    def delete_document(document_id: str, user_id: str) -> bool:
        """Delete document"""
        document = Database.execute_single_query(
            "SELECT user_id FROM documents WHERE id = %s", 
            (document_id,)
        )
        
        if not document or document['user_id'] != user_id:
            return False
        
        Database.execute_query("DELETE FROM documents WHERE id = %s", (document_id,))
        return True
    
    @staticmethod
    def search_documents(user_id: str, query: str, document_type: Optional[DocumentType] = None) -> List[DocumentResponse]:
        """Search documents by title or content"""
        search_term = f"%{query}%"
        
        if document_type:
            documents_data = Database.execute_query(
                "SELECT * FROM documents WHERE user_id = %s AND document_type = %s AND title LIKE %s ORDER BY updated_at DESC",
                (user_id, document_type, search_term),
                fetch=True
            )
        else:
            documents_data = Database.execute_query(
                "SELECT * FROM documents WHERE user_id = %s AND title LIKE %s ORDER BY updated_at DESC",
                (user_id, search_term),
                fetch=True
            )
        
        return [DocumentService._map_document_response(doc) for doc in documents_data]
    
    @staticmethod
    def _map_document_response(document_data: dict) -> DocumentResponse:
        """Map database record to DocumentResponse"""
        content = None
        if document_data.get('content'):
            try:
                content = json.loads(document_data['content'])
            except json.JSONDecodeError:
                content = document_data['content']
        
        return DocumentResponse(
            id=document_data['id'],
            user_id=document_data['user_id'],
            title=document_data['title'],
            document_type=document_data['document_type'],
            content=content,
            file_path=document_data.get('file_path'),
            file_size=document_data.get('file_size'),
            version=document_data.get('version', 1),
            created_at=document_data['created_at'],
            updated_at=document_data['updated_at']
        )