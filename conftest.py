import pytest
import requests
import allure
from urls import Urls
from helpers import register_new_courier_and_return_login_password

@pytest.fixture
def courier_setup():
    """Фикстура для создания курьера и его автоматического удаления"""
    courier_data = register_new_courier_and_return_login_password()
    
    if not courier_data:
        pytest.fail("Хелпер не смог создать курьера")

    payload = {
        "login": courier_data[0], 
        "password": courier_data[1]
    }
    
    with allure.step('Логин курьера в фикстуре для получения id'):
        response = requests.post(Urls.URL_LOGIN_COURIER, json=payload)
        courier_id = response.json().get("id")

    yield courier_data, courier_id

    if courier_id:
        with allure.step(f'Удаление курьера с id {courier_id} в фикстуре'):
             requests.delete(f"{Urls.URL_COURIER_ACTION}{courier_id}")

