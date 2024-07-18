from typing import Optional, Union
from sqlmodel import Field, SQLModel

class BaseProduct(SQLModel,table=True):
    id:Optional[int]= Field(default=None , primary_key=True)
    name:str = Field()
    price:float = Field()
    quantity:int = Field()
    shop_name:str = Field()

    