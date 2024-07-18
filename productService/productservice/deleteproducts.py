from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from productservice.db import get_session
from productservice.models import BaseProduct

router = APIRouter(
    tags=['Manage Products ALL','DELETE-Products']
)

@router.delete('/product/{id}')
def delete_product_by_id(id:int,db:Annotated[Session,Depends(get_session)]):
    product = db.exec(select(BaseProduct).filter(BaseProduct.id==id)).one()
    db.delete(product)
    db.commit()
    return {"message":"product deleted"}

@router.delete('/product')
def delete_product_by_shop_name(shop_name:str,db:Annotated[Session,Depends(get_session)]):
    product = db.exec(select(BaseProduct).filter(BaseProduct.shop_name==shop_name)).one()
    db.delete(product)
    db.commit()
    return {"message":"product deleted"}