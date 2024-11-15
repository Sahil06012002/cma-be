from typing import List

from fastapi import UploadFile
from models.schema import ProductCreate
from repository.product_repository import ProductRepository
from sqlalchemy.orm import Session

from services.blob_service import upload_images_to_blob


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.product_repository = ProductRepository(db)

    def create_product(self, product: ProductCreate, user_id: int):
        """
        Creates a new product for the provided user.
        """
        added_product = self.product_repository.add_product(product, user_id)
        return added_product

    def get_product_detail(self, id: int):
        """
        Fetches the details of a product by its ID.
        """
        product = self.product_repository.get_product_by_id(id)
        images = self.product_repository.get_images_by_product_id(id)
        return product , images
    
    async def get_all_products_by_user_id(self, user_id: int,keyword : str):
        if not keyword : 
            print("giving all the products")
            return self.product_repository.get_all_products_by_user_id(user_id)
        print("giving filtered the products")
        
        return await self.product_repository.search_product(user_id,keyword)
    
    def update_product(self, product_id: int, product_schema: ProductCreate):
        return self.product_repository.update_product(product_id, product_schema)
    
    def delete_product(self, product_id: int):
        return self.product_repository.delete_product(product_id)
    
    async def add_images_to_product_service(self, product_id: int, photos: List[UploadFile]) -> List[str]:
        image_urls = await upload_images_to_blob(photos)
        self.product_repository.add_images_to_product(product_id, image_urls)
        return image_urls
