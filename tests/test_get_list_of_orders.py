import requests
import allure
from urls import Urls
from data import TestData
from http import HTTPStatus

@allure.step("Создание нового заказа и получение трек-номера")
def get_new_order_track():
    payload = TestData.ORDER_DATA.copy()
    response = requests.post(Urls.URL_CREATE_ORDER, json=payload)
    return response.json().get("track")

@allure.title("Проверка получения заказа по его трек-номеру")
def test_get_order_by_track_success():
    track_number = get_new_order_track()
    
    with allure.step(f'Запрос данных заказа по треку {track_number}'):
         response = requests.get(f"{Urls.URL_CREATE_ORDER}/track", params={"t": track_number})
    
    assert response.status_code == HTTPStatus.OK
    assert "order" in response.json() 

@allure.title("Проверка получения списка заказов")
def test_get_orders_list_returns_success():
    with allure.step('Запрос общего списка заказов'):
        response = requests.get(Urls.URL_CREATE_ORDER)
    
    assert response.status_code == HTTPStatus.OK
    assert "orders" in response.json()
    assert isinstance(response.json().get("orders"), list)

