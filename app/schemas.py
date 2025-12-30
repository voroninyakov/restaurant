from pydantic import BaseModel
from uuid import UUID


class MenuModel(BaseModel):
    id: UUID = None
    title: str
    description: str


class DishModel(MenuModel):
    id: UUID = None
    title: str
    description: str
    price: float
