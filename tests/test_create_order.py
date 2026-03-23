import requests
import allure
import pytest
from urls import Urls
from data import TestData
from http import HTTPStatus

class TestCreateOrder:
    @allure.title('Создание заказа с разными вариантами цвета')
    @allure.description('Проверка выбора цвета: черный, серый, оба или отсутствие выбора')
    @pytest.mark.parametrize('chosen_color', TestData.ORDER_COLORS) 
    def test_create_order_with_different_colors(self, chosen_color):
        payload = TestData.ORDER_DATA.copy()
        payload['color'] = chosen_color
        
        with allure.step(f'Отправка запроса на создание заказа с цветом: {chosen_color}'):
            response = requests.post(Urls.URL_CREATE_ORDER, json=payload, timeout=10)
        
        assert response.status_code == HTTPStatus.CREATED
        assert 'track' in response.json()

