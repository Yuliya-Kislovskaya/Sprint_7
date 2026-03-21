import requests
import allure
import pytest
from data import TestData
from helpers import register_new_courier_and_return_login_password
from urls import Urls
from http import HTTPStatus

class TestCreateCourier:
    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self):
        # Метод из условия возвращает [login, password, name] при успехе
        result = register_new_courier_and_return_login_password()
        assert len(result) == 3 

    @allure.title('Ошибка при создании дубликата курьера')
    def test_create_duplicate_courier(self):
        # 1. Создаем первого курьера
        first_courier = register_new_courier_and_return_login_password()
        
        # 2. Пытаемся создать курьера с тем же логином (индекс 0)
        payload = {
            "login": first_courier[0],
            "password": "another_password",
            "firstName": "another_name"
        }
        
        response = requests.post(Urls.URL_CREATE_COURIER, json=payload)
        
        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json()["message"] == TestData.MESSAGE_CONFLICT["message"]

    @allure.title('Ошибка 400 при отсутствии обязательного поля')
    @pytest.mark.parametrize('fields', [
        {'password': 'password123', 'firstName': 'Violetta'}, # Нет поля login
        {'login': 'Violetta_777', 'firstName': 'Violetta'},   # Нет поля password
        {'firstName': 'Violetta'}                            # Нет и логина, и пароля
    ])
    def test_create_courier_missing_fields(self, fields):
        # Отправляем запрос без одного из обязательных полей
        response = requests.post(Urls.URL_CREATE_COURIER, json=fields)
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["message"] == TestData.MESSAGE_BAD_REQUEST["message"]



