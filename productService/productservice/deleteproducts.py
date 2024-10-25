from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select,delete

from productservice.db import get_session
from productservice.models import BaseProduct

router = APIRouter(
    tags=['Manage Products ALL','DELETE-Products']
)

@router.delete('/product')
def delete_by_id_or_shopname(
    db: Annotated[Session, Depends(get_session)],
    id: int = None,
    shop_name: str = None,
    delete_all_products: bool = False
):
    # Validate that delete_all_products must be True if shop_name is provided and id is not provided
    if shop_name and not delete_all_products and not id:
        raise HTTPException(status_code=400, detail="delete_all_products must be True if shop_name is provided without an id.")
    
    # Ensure that only id or shop_name with delete_all_products=True is provided, not both
    if id and shop_name:
        raise HTTPException(status_code=400, detail="Provide either 'id' or 'shop_name' with 'delete_all_products=True', but not both.")

    # Delete by ID if id is provided without shop_name
    if id:
        if delete_all_products:
            raise HTTPException(status_code=400,detail="delete_all_product must be false when sending id as query")
        product = db.exec(select(BaseProduct).filter(BaseProduct.id == id)).one()
        db.delete(product)
        db.commit()
        return {"message": "product deleted"}
    
    # Delete all products by shop_name if delete_all_products is True
    if shop_name and delete_all_products:
        db.exec(delete(BaseProduct).where(BaseProduct.shop_name == shop_name))
        db.commit()
        return {"message": "all products deleted"}
    
    # Raise exception if neither id nor shop_name with delete_all_products is given
    raise HTTPException(
        status_code=400,
        detail="Provide either 'id' or 'shop_name' with 'delete_all_products=True/False'."
    )

