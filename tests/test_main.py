from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from app.models import Base
from app.main import app, get_db
from app.config import *

menu_id = None

TEST_DATABASE_URL = f'postgresql://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'

engine = create_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_menus_get():
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/api/v1/menus", json={"title": "My menu 1", "description": "My menu description 1"})
    assert response.status_code == 201
    assert 'id' in response.json().keys()
    menu_id = response.json()["id"]
    assert 'title' in response.json().keys()
    assert 'description' in response.json().keys()

    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() != []

    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert 'id' in response.json().keys()
    assert 'title' in response.json().keys()
    assert 'description' in response.json().keys()

    response = client.patch(f'/api/v1/menus/{menu_id}',
                            json={"title": "My updated menu 1", "description": "My updated menu description 1"})
    assert response.status_code == 200
    assert 'id' in response.json().keys()
    assert 'title' in response.json().keys()
    assert 'description' in response.json().keys()

    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert 'id' in response.json().keys()
    assert 'title' in response.json().keys()
    assert 'description' in response.json().keys()

    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": True, "message": "The menu has been deleted"}

    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}

    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []


def test_dishes_and_submenus_count():
    response = client.post("/api/v1/menus", json={"title": "My menu 1", "description": "My menu description 1"})
    assert response.status_code == 201
    assert 'id' in response.json().keys()
    menu_id = response.json()["id"]
    assert 'title' in response.json().keys()
    assert 'description' in response.json().keys()

    response = client.post(f"/api/v1/menus/{menu_id}/submenus/", json={"title": "My submenu 1",
                                                                       "description": "My submenu description 1"})
    assert response.status_code == 201
    assert 'id' in response.json().keys()
    submenu_id = response.json()["id"]
    assert 'title' in response.json().keys()
    assert 'description' in response.json().keys()

    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
                           json={"title": "My dish 1",
                                 "description": "My dish description 1",
                                 "price": "13.50"
                                 })
    assert response.status_code == 201
    assert 'id' in response.json().keys()
    assert 'title' in response.json().keys()
    assert 'description' in response.json().keys()
    assert 'price' in response.json().keys()

    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
                           json={"title": "My dish 2",
                                 "description": "My dish description 2",
                                 "price": "13.50"
                                 })
    assert response.status_code == 201
    assert 'id' in response.json().keys()
    assert 'title' in response.json().keys()
    assert 'description' in response.json().keys()
    assert 'price' in response.json().keys()

    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert 'id' in response.json().keys()
    assert 'title' in response.json().keys()
    assert 'description' in response.json().keys()

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert 'id' in response.json().keys()
    assert 'title' in response.json().keys()
    assert 'description' in response.json().keys()

    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": True, "message": "The submenu has been deleted"}

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/")
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert 'id' in response.json().keys()
    assert 'title' in response.json().keys()
    assert 'description' in response.json().keys()

    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": True, "message": "The menu has been deleted"}

    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []
