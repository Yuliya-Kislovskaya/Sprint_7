import pytest
import requests
import allure
from urls import Urls
from helpers import register_new_courier_and_return_login_password
from http import HTTPStatus

@pytest.fixture
def courier_setup():
   
    courier_data = register_new_courier_and_return_login_password()
    
    if not courier_data:
        pytest.fail("Хелпер не смог создать курьера")

    payload = {"login": courier_data[0], "password": courier_data[1]}
    
    with allure.step('Логин курьера в фикстуре для получения id'):
        response = requests.post(Urls.URL_LOGIN_COURIER, json=payload)
        courier_id = response.json().get("id")

    yield courier_data, courier_id

    if courier_id:
        with allure.step(f'Удаление курьера с id {courier_id} в фикстуре'):
             requests.delete(f"{Urls.URL_COURIER_ACTION}{courier_id}")

@pytest.fixture
def delete_courier():
    couriers_to_clean = []
    yield couriers_to_clean
    
    for courier in couriers_to_clean:
        with allure.step(f'Логин курьера {courier[0]} для получения id'):
            login_payload = {"login": courier[0], "password": courier[1]}
            login_response = requests.post(Urls.URL_LOGIN_COURIER, json=login_payload)
        
        if login_response.status_code == HTTPStatus.OK:
            courier_id = login_response.json().get("id")
            with allure.step(f'Удаление курьера с id {courier_id}'):
                 requests.delete(f"{Urls.URL_COURIER_ACTION}{courier_id}")
