import pytest
import requests
from urls import Urls
from helpers import register_new_courier_and_return_login_password

@pytest.fixture
def courier_setup():
    """Фикстура для создания курьера и его автоматического удаления"""
    courier_data = register_new_courier_and_return_login_password()
    
    payload = {"login": courier_data[0], "password": courier_data[1]}
    response = requests.post(Urls.URL_LOGIN_COURIER, json=payload)
    courier_id = response.json().get("id")

    yield courier_data, courier_id

    if courier_id:
        requests.delete(f"{Urls.URL_CREATE_COURIER}/{courier_id}")
