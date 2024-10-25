from typing import Annotated, List, Optional, Union
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from productservice.db import get_session
from productservice.models import BaseProduct

router = APIRouter(
    tags=['Manage Products ALL' , 'GET-Products']
)

@router.get('/product',response_model=Union[BaseProduct,list[BaseProduct]])
def get_all_products_or_search_by_id_or_shopname(db:Annotated[Session,Depends(get_session)],id:Optional[int]=None,shopname:Optional[str]=None):
    if id:
        product = db.exec(select(BaseProduct).filter(BaseProduct.id==id)).one()
        return product    
    if shopname:
        product = db.exec(select(BaseProduct).filter(BaseProduct.shop_name==shopname)).all()
        return product    
    products = db.exec(select(BaseProduct))
    return products