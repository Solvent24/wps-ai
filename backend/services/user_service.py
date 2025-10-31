import uuid
from typing import Optional, List
from database.database import Database
from models.models import UserCreate, UserResponse, UserLogin
from auth.auth import get_password_hash, verify_password

class UserService:
    @staticmethod
    def create_user(user: UserCreate) -> UserResponse:
        """Create new user"""
        # Check if user already exists
        existing_user = Database.execute_single_query(
            "SELECT id FROM users WHERE email = %s", 
            (user.email,)
        )
        
        if existing_user:
            raise ValueError("User with this email already exists")
        
        user_id = str(uuid.uuid4())
        password_hash = get_password_hash(user.password)
        
        Database.execute_query(
            "INSERT INTO users (id, email, name, password_hash) VALUES (%s, %s, %s, %s)",
            (user_id, user.email, user.name, password_hash)
        )
        
        # Create user settings
        Database.execute_query(
            "INSERT INTO user_settings (user_id) VALUES (%s)",
            (user_id,)
        )
        
        return UserService.get_user_by_id(user_id)
    
    @staticmethod
    def authenticate_user(login: UserLogin) -> Optional[UserResponse]:
        """Authenticate user"""
        user_data = Database.execute_single_query(
            "SELECT * FROM users WHERE email = %s", 
            (login.email,)
        )
        
        if not user_data:
            return None
        
        if not verify_password(login.password, user_data['password_hash']):
            return None
        
        return UserResponse(
            id=user_data['id'],
            email=user_data['email'],
            name=user_data['name'],
            created_at=user_data['created_at'],
            updated_at=user_data['updated_at']
        )
    
    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[UserResponse]:
        """Get user by ID"""
        user_data = Database.execute_single_query(
            "SELECT * FROM users WHERE id = %s", 
            (user_id,)
        )
        
        if not user_data:
            return None
        
        return UserResponse(
            id=user_data['id'],
            email=user_data['email'],
            name=user_data['name'],
            created_at=user_data['created_at'],
            updated_at=user_data['updated_at']
        )
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[UserResponse]:
        """Get user by email"""
        user_data = Database.execute_single_query(
            "SELECT * FROM users WHERE email = %s", 
            (email,)
        )
        
        if not user_data:
            return None
        
        return UserResponse(
            id=user_data['id'],
            email=user_data['email'],
            name=user_data['name'],
            created_at=user_data['created_at'],
            updated_at=user_data['updated_at']
        )
    
    @staticmethod
    def update_user(user_id: str, updates: dict) -> Optional[UserResponse]:
        """Update user information"""
        allowed_fields = ['name', 'email']
        update_fields = []
        params = []
        
        for field in allowed_fields:
            if field in updates:
                update_fields.append(f"{field} = %s")
                params.append(updates[field])
        
        if not update_fields:
            return UserService.get_user_by_id(user_id)
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
        
        Database.execute_query(query, params)
        return UserService.get_user_by_id(user_id)
    
    @staticmethod
    def get_user_settings(user_id: str) -> dict:
        """Get user settings"""
        settings = Database.execute_single_query(
            "SELECT * FROM user_settings WHERE user_id = %s", 
            (user_id,)
        )
        
        return settings or {}
    
    @staticmethod
    def update_user_settings(user_id: str, settings: dict) -> dict:
        """Update user settings"""
        allowed_fields = ['theme', 'language', 'auto_save', 'ai_assistance']
        update_fields = []
        params = []
        
        for field in allowed_fields:
            if field in settings:
                update_fields.append(f"{field} = %s")
                params.append(settings[field])
        
        if update_fields:
            params.append(user_id)
            query = f"UPDATE user_settings SET {', '.join(update_fields)} WHERE user_id = %s"
            Database.execute_query(query, params)
        
        return UserService.get_user_settings(user_id)