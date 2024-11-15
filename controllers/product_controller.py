from typing import List

from fastapi import File, UploadFile
from models.db_models import Image
from models.schema import ProductCreate
from sqlalchemy.orm import Session

from services.product_service import ProductService


class ProductController:
    def __init__(self, db: Session):
        self.db = db
        self.product_service = ProductService(db)

    async def create_product(self, product: ProductCreate,user_id: int,photos: List[UploadFile] = File(None)):
        added_product = self.product_service.create_product(product, user_id)
        if photos:
            print("printing image")
            # await self.product_service.add_images_to_product_service(added_product.id,photos)
        return added_product


    def get_product_detail(self, id: int):
        return self.product_service.get_product_detail(id)

    async def get_all_products_by_user_id(self, user_id: int,keyword : str):
        return await self.product_service.get_all_products_by_user_id(user_id,keyword)

    
    def update_product(self, product_id: int, product_schema: ProductCreate):
        return self.product_service.update_product(product_id, product_schema)
    
    def delete_product(self, product_id: int):
        return self.product_service.delete_product(product_id)
    
        
    