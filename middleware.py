from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from models.db_models import User
from database import get_db
from services.auth import verify_token

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("req path-----")
        print(request.url.path)
        if request.url.path in ["/api/user/login", "/api/user/signup","/api/docs","/api/openapi.json"]:
            return await call_next(request)

        token = request.headers.get("Authorization")
        if token is None or not token.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Authorization token missing"})
        
        token = token[7:]  # Removing "Bearer " prefix

        try:
            user_id: int = verify_token(token)
            if not user_id :
                raise HTTPException(status_code=401, detail="Invalid token payload")
            
            db: Session =  next(get_db())
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=401, detail="Invalid user ID")
            
            request.state.user_id = user_id

        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})
        
        response = await call_next(request)
        return response
