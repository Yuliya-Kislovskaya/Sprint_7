import requests
import allure
import pytest
from data import TestData
from helpers import register_new_courier_and_return_login_password
from urls import Urls
from http import HTTPStatus

class TestCreateCourier:

    @pytest.fixture
    def delete_courier(self):
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

    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self, delete_courier):
        with allure.step('Регистрация нового курьера через хелпер'):
            result = register_new_courier_and_return_login_password()
        
        delete_courier.append([result[0], result[1]])
        
        assert len(result) == 3

    @allure.title('Ошибка при создании дубликата курьера')
    def test_create_duplicate_courier(self, delete_courier):
        with allure.step('Создание первого курьера'):
            first_courier = register_new_courier_and_return_login_password()
            delete_courier.append([first_courier[0], first_courier[1]])
        
        payload = {
            "login": first_courier[0],
            "password": TestData.CORRECT_PASSWORD,
            "firstName": TestData.CORRECT_NAME
        }
        
        with allure.step('Отправка запроса на создание дубликата с тем же логином'):
            response = requests.post(Urls.URL_CREATE_COURIER, json=payload)
        
        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json()["message"] == TestData.MESSAGE_CONFLICT["message"]

    @allure.title('Ошибка 400 при отсутствии обязательного поля')
    @pytest.mark.parametrize('fields', TestData.MISSING_FIELDS_DATA)
    def test_create_courier_missing_fields(self, fields):
        with allure.step('Отправка запроса с неполными данными из TestData'):
            response = requests.post(Urls.URL_CREATE_COURIER, json=fields)
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["message"] == TestData.MESSAGE_BAD_REQUEST["message"]