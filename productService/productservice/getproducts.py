from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from productservice.db import get_session
from productservice.models import BaseProduct

router = APIRouter(
    tags=['Manage Products ALL' , 'GET-Products']
)

@router.get('/product',response_model=list[BaseProduct])
def read_all_product(db:Annotated[Session,Depends(get_session)])->List[BaseProduct]:
    products = db.exec(select(BaseProduct))
    return products

@router.get('/product/{id}',response_model=BaseProduct)
def read_products_by_id(id:int,db:Annotated[Session,Depends(get_session)])->BaseProduct:
    product = db.exec(select(BaseProduct).filter(BaseProduct.id==id)).one()
    return product

@router.get('/product/shop{shop_name}',response_model=BaseProduct)
def read_products_by_shop_name(shop_name:str,db:Annotated[Session,Depends(get_session)])->BaseProduct:
    product = db.exec(select(BaseProduct).filter(BaseProduct.shop_name==shop_name)).one()
    return product