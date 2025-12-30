from fastapi import FastAPI, status, Depends
from schemas import *
from models import Menu, select, Submenu, Dish
from database import SessionLocal, engine, Base
from fastapi.responses import JSONResponse
from uuid import UUID
import uvicorn

Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# menu
@app.post("/api/v1/menus", status_code=201)
def create_menu(create: MenuModel):
    session = next(get_db())
    menu = Menu(create.title, create.description)
    response = menu.json()
    session.add(menu)
    session.commit()
    return response


@app.patch("/api/v1/menus/{menu_id}/")
def update_menu(menu_id: UUID, create: MenuModel):
    session = next(get_db())
    menu = session.query(Menu).get(menu_id)
    menu.title, menu.description = create.title, create.description
    if menu:
        response = menu.json()
    else:
        response = JSONResponse({'detail': 'menu not found'}, 404)
    session.commit()
    return response


@app.delete("/api/v1/menus/{menu_id}/")
def delete_menu(menu_id: UUID):
    session = next(get_db())
    menu = session.query(Menu).get(menu_id)
    if menu:
        for submenu in menu.submenus:
            for dish in submenu.dishes:
                session.delete(dish)
            session.delete(submenu)
        session.delete(menu)
        response = {"status": True, "message": "The menu has been deleted"}
    else:
        response = JSONResponse({'detail': 'menu not found'}, 404)
    session.commit()
    return response


@app.get("/api/v1/menus")
def read_menu_list():
    session = next(get_db())
    menus = session.query(Menu)
    session.commit()
    return [menu.json() for menu in menus]


@app.get("/api/v1/menus/{menu_id}/")
def read_menu(menu_id: UUID):
    session = next(get_db())
    menu = session.query(Menu).get(menu_id)
    if menu:
        response = menu.json()
    else:
        response = JSONResponse({'detail': 'menu not found'}, 404)
    return response

# submenus


@app.get("/api/v1/menus/{menu_id}/submenus/")
def read_submenu_list(menu_id: UUID):
    session = next(get_db())
    menu = session.query(Menu).get(menu_id)
    if menu:
        submenus = menu.submenus
        response = [submenu.json() for submenu in submenus]
    else:
        response = JSONResponse({'detail': 'menu not found'}, 404)
    session.commit()
    return response


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/")
def read_submenu(submenu_id: UUID):
    session = next(get_db())
    submenu = session.query(Submenu).get(submenu_id)
    if submenu:
        response = submenu.json()
    else:
        response = JSONResponse({'detail': 'submenu not found'}, 404)

    return response


@app.post("/api/v1/menus/{menu_id}/submenus/", status_code=201)
def create_submenu(menu_id: UUID, create: MenuModel):
    session = next(get_db())
    submenu = Submenu(create.title, create.description, menu_id)
    response = submenu.json()
    session.add(submenu)
    session.commit()
    return response


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/")
def update_submenu(submenu_id: UUID, create: MenuModel):
    session = next(get_db())
    submenu = session.query(Submenu).get(submenu_id)
    if submenu:
        submenu.title, submenu.description = create.title, create.description
        response = submenu.json()
        session.commit()
    else:
        response = JSONResponse({'detail': 'submenu not found'}, 404)

    return response


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/")
def delete_submenu(submenu_id: UUID,):
    session = next(get_db())
    submenu = session.query(Submenu).get(submenu_id)
    if submenu:
        for dish in list(submenu.dishes):
            session.delete(dish)
        session.delete(submenu)
        response = {"status": True, "message": "The submenu has been deleted"}
    else:
        response = JSONResponse({'detail': 'submenu not found'}, 404)
    session.commit()
    return response

# dishes


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
def read_dish_list(submenu_id: UUID):
    session = next(get_db())
    submenu = session.query(Submenu).get(submenu_id)
    if submenu:
        dishes = submenu.dishes
        response = [dish.json() for dish in dishes]
    else:
        response = []
    session.commit()
    return response


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def read_dish(dish_id: UUID):
    session = next(get_db())
    dish = session.query(Dish).get(dish_id)
    if dish:
        response = dish.json()
    else:
        response = JSONResponse({'detail': 'dish not found'}, 404)

    return response


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", status_code=201)
def create_dish(menu_id: UUID, submenu_id: UUID, create: DishModel):
    session = next(get_db())
    submenu = session.query(Submenu).get(submenu_id)
    if submenu:
        dish = Dish(create.title, create.description, create.price, submenu_id)
        response = dish.json()
        session.add(dish)
    else:
        response = JSONResponse({'detail': 'submenu not found'}, 404)
    session.commit()
    return response


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def update_dish(dish_id: UUID, create: DishModel):
    session = next(get_db())
    dish = session.query(Dish).get(dish_id)
    dish.title, dish.description, dish.price = create.title, create.description, create.price
    if dish:
        response = dish.json()
    else:
        response = JSONResponse({'detail': 'dish not found'}, 404)
    session.commit()
    return response


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(dish_id: UUID):
    session = next(get_db())
    dish = session.query(Dish).get(dish_id)
    if dish:
        session.delete(dish)
        response = {"status": True, "message": "The dish has been deleted"}
    else:
        response = JSONResponse({'detail': 'dish not found'}, 404)
    session.commit()
    return response


