from typing import List
from models.db_models import Image, Product
from models.schema import ProductCreate
from sqlalchemy.orm import Session



class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def add_product(self, product_schema : ProductCreate,user_id: int) :
        dumped_data = product_schema.model_dump(exclude_unset=True)
        new_product = Product(**dumped_data)
        new_product.user_id = user_id
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product
    
    def get_product_by_id(self,id : int) :
        product = self.db.query(Product).filter(Product.id == id).first()
        return product

    def get_all_products_by_user_id(self, user_id: int):
        products = self.db.query(Product).filter(Product.user_id == user_id).all()
        return products
    
    def update_product(self, product_id: int, product_schema: ProductCreate):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None 
        
        updated_data = product_schema.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(product, key, value)

        self.db.commit()
        self.db.refresh(product)

        return product
    
    def delete_product(self, product_id: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None
        
        self.db.delete(product)
        self.db.commit()
        return product_id
    
    def add_images_to_product(self, product_id: int, image_urls: List[str]) -> None:
        for url in image_urls:
            image = Image(product_id=product_id, image_url=url)
            self.db.add(image)
        self.db.commit()


    async def search_product(self, user_id: int,keyword: str):
        products = self.db.query(Product).filter(
            Product.user_id == user_id,
            (Product.title.ilike(f"%{keyword}%")) |
            (Product.description.ilike(f"%{keyword}%")) |
            (Product.product_tag.ilike(f"%{keyword}%"))
        ).all()
        return products