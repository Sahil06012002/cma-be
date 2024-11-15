from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from controllers.product_controller import ProductController
from models.schema import ProductCreate
from database import get_db

router = APIRouter()



@router.post("",tags=["product"]) 
async def add_product(
    request: Request,
    title: str = Form(...),  
    description: Optional[str] = Form(None),  
    product_tag: Optional[str] = Form(None),  
    company: Optional[str] = Form(None),
    dealer: Optional[str] = Form(None), 
    photos: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
) :
    print("check=====>")
    user_id = request.state.user_id

    product_controller = ProductController(db)
    product_schema = ProductCreate(
        title=title,
        description=description,
        product_tag=product_tag,
        company=company,
        dealer=dealer,
    )
    added_product = await product_controller.create_product(product_schema,user_id,photos)
    print(added_product.description)
    return {"added product" : added_product}

@router.get("",tags=["product"])
async def get_all_products_by_user_id(request: Request,db: Session = Depends(get_db), keyword: Optional[str] = None) : 
    user_id = request.state.user_id   
    product_controller = ProductController(db)
    product = await product_controller.get_all_products_by_user_id(user_id,keyword)
    return {"product list" : product}

@router.get("/{product_id}",tags=["product"])
async def get_product_details(product_id: int,db: Session = Depends(get_db)) : 
    print("fe check")
    product_controller = ProductController(db)
    product, images = product_controller.get_product_detail(product_id)
    return {"product details" : product, "product_images" : images}

@router.put("/{product_id}",tags=["product"])
async def update_product(
    product_id: int,
    product_schema: ProductCreate,
    db: Session = Depends(get_db),
):
    product_controller = ProductController(db)
    updated_product = product_controller.update_product(product_id, product_schema)
    
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"updated product": updated_product}

@router.delete("/{product_id}",tags=["product"])
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product_controller = ProductController(db)
    result = product_controller.delete_product(product_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")  
    return {"deleted product": result}

