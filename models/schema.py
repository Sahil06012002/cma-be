from typing import Optional
from pydantic import BaseModel

class UserAPI(BaseModel):
    username: str
    password: str
    email : str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductCreate(BaseModel) :
    title : str
    description : Optional[str] = None
    product_tag : Optional[str] = None
    company : Optional[str] = None
    dealer : Optional[str] = None

