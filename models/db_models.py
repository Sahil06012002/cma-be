from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import validates
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)

    products = relationship("Product", back_populates="user")



class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    product_tag = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    dealer = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User", back_populates="products")
    images = relationship("Image", back_populates="product", cascade="all, delete-orphan")


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    image_url = Column(String, nullable=False)

    product = relationship("Product", back_populates="images")



