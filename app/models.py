from typing import List
from sqlalchemy import ForeignKey, String, Float, create_engine, Uuid, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from database import Base
from uuid import UUID
import uuid


class Menu(Base):
    __tablename__ = 'menu_table'
    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    submenus: Mapped[List["Submenu"]] = relationship()

    def __init__(self, title, description):
        self.id = uuid.uuid4()
        self.title = title
        self.description = description

    def __repr__(self) -> str:
        return f"Menu(id={self.id!r}, title={self.title!r}, description={self.description!r})"

    @property
    def submenus_count(self):
        return len(self.submenus)

    @property
    def dishes_count(self):
        dishes = 0
        for submenu in self.submenus:
            dishes += len(submenu.dishes)
        return dishes

    def json(self):
        json = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'submenus_count': self.submenus_count,
            'dishes_count': self.dishes_count
        }
        return json


class Submenu(Base):
    __tablename__ = 'submenu_table'
    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    menu_id: Mapped[Uuid] = mapped_column(ForeignKey("menu_table.id"))
    dishes: Mapped[List["Dish"]] = relationship()

    def __init__(self, title, description, menu_id):
        self.id = uuid.uuid4()
        self.menu_id = menu_id
        self.title = title
        self.description = description

    def __repr__(self) -> str:
        return f"Submenu(id={self.id!r}, name={self.title!r})"

    def json(self):
        json = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'dishes_count': len(self.dishes)
        }
        return json


class Dish(Base):
    __tablename__ = 'dish_table'
    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    submenu_id: Mapped[Uuid] = mapped_column(ForeignKey("submenu_table.id"))

    def __repr__(self) -> str:
        return f"Dish(id={self.id!r}, title={self.title!r}, price={self.price!r})"

    def __init__(self, title, description, price, submenu_id):
        self.id = uuid.uuid4()
        self.submenu_id = submenu_id
        self.title = title
        self.description = description
        self.price = price

    def json(self):
        json = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': "{:.2f}".format(self.price),
        }
        return json
