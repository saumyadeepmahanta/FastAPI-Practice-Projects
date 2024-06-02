from .utils import *
from ..routers.users import get_current_user,get_db
from fastapi import status


app.dependency_overrides[get_current_user]=override_get_current_user
app.dependency_overrides[get_db]=override_get_db

def test_return_user(test_user):
    response=client.get("/")
    assert response.status_code==status.HTTP_200_OK