from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from models.schema import Token, UserAPI
from repository.user_repository import UserRepository
from services.auth import create_access_token, hash_password, verify_password, verify_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup",tags=["user"])
async def signup(user: UserAPI, db: Session = Depends(get_db)):
    print(user.username,"password-----<",user.password,user.email)
    user_repository = UserRepository(db)

    existing_user = user_repository.get_user_by_username(user.username)
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    new_user = user_repository.create_user(user.username, hashed_password, user.email)
    return {"message": f"User {new_user.username} created successfully"}

@router.post("/login", response_model=Token,tags=["user"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_username(form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(hours=24)
    access_token = access_token = create_access_token(
        data={"username": user.username, "id": user.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

