import requests
import allure
import pytest
from http import HTTPStatus
from urls import Urls
from data import TestData

class TestLoginCourier:
    @allure.title('Успешная авторизация курьера')
    def test_courier_login_valid_data(self, courier_setup):
        payload = {
            "login": courier_setup[0][0],
            "password": courier_setup[0][1]
        }
        
        response = requests.post(Urls.URL_LOGIN_COURIER, json=payload)
        
        assert response.status_code == HTTPStatus.OK
        assert 'id' in response.json()

    @allure.title('Ошибка при логине с незаполненным полем')
    @pytest.mark.parametrize('fields', [
        {'login': '', 'password': TestData.CORRECT_PASSWORD},
        {'login': TestData.CORRECT_LOGIN, 'password': ''},
    ])
    def test_courier_login_with_empty_fields(self, fields):
        response = requests.post(Urls.URL_LOGIN_COURIER, json=fields)
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["message"] == TestData.MESSAGE_LOGIN_BAD_REQUEST["message"]

    @allure.title('Ошибка при авторизации под несуществующим пользователем')
    def test_courier_login_with_invalid_data(self):
        random_payload = {
            'login': 'non_existent_ninja_777', 
            'password': 'wrong_password_999'
        }
        response = requests.post(Urls.URL_LOGIN_COURIER, json=random_payload)
        
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["message"] == TestData.MESSAGE_NOT_FOUND["message"]



