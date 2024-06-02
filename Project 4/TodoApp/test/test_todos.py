from ..routers.todos import get_db,get_current_user
from fastapi import status
from ..models import Todos
from .utils import *


# Apply dependency overrides
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": test_todo.id,
        "title": "Learn to code!",
        "description": "Need to learn everyday",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }]

def test_read_one(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": test_todo.id,
        "title": "Learn to code!",
        "description": "Need to learn everyday",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }
    
    

def test_create_todo(test_todo):
    request_data={
        "title":"New Todo",
        "description":"New Todo Descrption",
        "priority":5,
        "complete":False,
    }
    response=client.post("/todo/",json=request_data)
    assert response.status_code==201
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==2).first()
    assert model.title==request_data.get("title")
    
def test_update_todo(test_todo):
    request_data={
        "title":"change title",
        "description":"Need to learn everyday",
        "priority":5,
        "complete":False,
    }
    response=client.put("/todo/1",json=request_data)
    assert response.status_code==204
    
def test_delete_todo(test_todo):
    response=client.delete("/todo/1")
    assert response.status_code==204