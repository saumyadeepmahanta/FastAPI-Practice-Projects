from .utils import *
from ..routers .admin import get_current_user,get_db
from fastapi import status
from ..models import Todos

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_admin_real_all_authenticates(test_todo):
    response=client.get("/admin/todo")
    assert response.status_code==status.HTTP_200_OK
    
def test_admin_delete_todo(test_todo):
    response=client.delete("/admin/todo/1")
    assert response.status_code==204
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model is None