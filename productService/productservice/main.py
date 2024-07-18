from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from productservice import deleteproducts, getproducts
from productservice.db import get_session, lifespan
from productservice.models import BaseProduct

app = FastAPI(
    title="Product Service",
    lifespan=lifespan,
)

app.include_router(getproducts.router)
app.include_router(deleteproducts.router)

@app.post('/product',tags=['Manage Products ALL'],response_model=BaseProduct)
def create_product(product:BaseProduct,db:Annotated[Session,Depends(get_session)])->BaseProduct:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.patch('/product',tags=['Manage Products ALL'],response_model=BaseProduct)
def update_product(product:BaseProduct,db:Annotated[Session,Depends(get_session)])->BaseProduct:
    prod:BaseProduct = db.exec(select(BaseProduct).filter(BaseProduct.id==product.id)).first()
    update_product = product.model_dump(exclude_unset=True)
    prod.sqlmodel_update(update_product)
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return product



