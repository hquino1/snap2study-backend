from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config import get_settings
from supabase import create_client, ClientOptions

settings = get_settings()
security = HTTPBearer()


def verify_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        client = create_client(
            settings.SUPABASE_URL, 
            settings.SUPABASE_KEY,
            options=ClientOptions(
                    headers={"Authorization": f"Bearer {token}"}
                )
            )
    
        user = client.auth.get_user(token)
        return client, user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
