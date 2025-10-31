from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import os
from dotenv import load_dotenv
from database.database import Database
from auth.auth import create_access_token
from models.models import UserResponse, Token
import uuid
from typing import Optional

load_dotenv()

router = APIRouter(prefix="/auth", tags=["authentication"])

# OAuth Configuration
oauth = OAuth()

# Register Google OAuth
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8000/auth/callback')
    }
)

@router.get("/google/login")
async def google_login(request: Request):
    """Redirect to Google OAuth login"""
    try:
        redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8000/auth/callback')
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth configuration error: {str(e)}"
        )

@router.get("/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback"""
    try:
        # Get the token from Google
        token = await oauth.google.authorize_access_token(request)
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get access token from Google"
            )
        
        # Get user info from Google
        user_info = token.get('userinfo')
        
        if not user_info:
            # Try to get user info manually
            user_info = await oauth.google.userinfo(token=token)
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user information from Google"
            )
        
        # Extract user data
        email = user_info.get('email')
        name = user_info.get('name', 'User')
        google_id = user_info.get('sub')
        picture = user_info.get('picture')
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by Google"
            )
        
        print(f"Google OAuth successful for: {email}")  # Debug log
        
        # Find or create user
        user = await find_or_create_user(email, name, google_id, picture)
        
        # Create JWT token
        access_token = create_access_token(data={"sub": user.id})
        
        # Redirect to frontend with token
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        redirect_url = f"{frontend_url}/auth/success?token={access_token}&user_id={user.id}"
        
        return RedirectResponse(url=redirect_url)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"OAuth callback error: {str(e)}")  # Debug log
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        error_message = f"Authentication failed: {str(e)}"
        encoded_message = error_message.replace(' ', '%20')
        error_url = f"{frontend_url}/auth/error?message={encoded_message}"
        return RedirectResponse(url=error_url)

async def find_or_create_user(email: str, name: str, google_id: str, picture: Optional[str] = None) -> UserResponse:
    """Find existing user or create new one with Google OAuth"""
    
    try:
        # Check if user already exists by email
        existing_user = Database.execute_single_query(
            "SELECT * FROM users WHERE email = %s", 
            (email,)
        )
        
        if existing_user:
            # Update Google ID if not set
            if not existing_user.get('google_id'):
                Database.execute_query(
                    "UPDATE users SET google_id = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (google_id, existing_user['id'])
                )
            
            return UserResponse(
                id=existing_user['id'],
                email=existing_user['email'],
                name=existing_user['name'],
                created_at=existing_user['created_at'],
                updated_at=existing_user['updated_at']
            )
        
        # Check if user exists by Google ID (shouldn't happen but just in case)
        existing_google_user = Database.execute_single_query(
            "SELECT * FROM users WHERE google_id = %s", 
            (google_id,)
        )
        
        if existing_google_user:
            return UserResponse(
                id=existing_google_user['id'],
                email=existing_google_user['email'],
                name=existing_google_user['name'],
                created_at=existing_google_user['created_at'],
                updated_at=existing_google_user['updated_at']
            )
        
        # Create new user
        user_id = str(uuid.uuid4())
        
        Database.execute_query(
            """
            INSERT INTO users (id, email, name, google_id, password_hash)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, email, name, google_id, 'oauth_user')  # Empty password for OAuth users
        )
        
        # Create user settings
        Database.execute_query(
            "INSERT INTO user_settings (user_id) VALUES (%s)",
            (user_id,)
        )
        
        # Get the created user
        new_user = Database.execute_single_query(
            "SELECT * FROM users WHERE id = %s", 
            (user_id,)
        )
        
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        return UserResponse(
            id=new_user['id'],
            email=new_user['email'],
            name=new_user['name'],
            created_at=new_user['created_at'],
            updated_at=new_user['updated_at']
        )
        
    except Exception as e:
        print(f"Error in find_or_create_user: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/test")
async def test_oauth():
    """Test endpoint to verify OAuth configuration"""
    return {
        "client_id": os.getenv('GOOGLE_OAUTH_CLIENT_ID') is not None,
        "client_secret": os.getenv('GOOGLE_OAUTH_CLIENT_SECRET') is not None,
        "redirect_uri": os.getenv('GOOGLE_REDIRECT_URI'),
        "status": "OAuth configured"
    }

@router.get("/success")
async def auth_success(token: str, user_id: str):
    """Auth success endpoint - can be used for direct API calls"""
    return JSONResponse({
        "message": "Authentication successful",
        "access_token": token,
        "token_type": "bearer",
        "user_id": user_id
    })

@router.get("/error")
async def auth_error(message: str):
    """Auth error endpoint"""
    return JSONResponse({
        "error": "Authentication failed",
        "message": message
    }, status_code=400)