import requests
import allure
from urls import Urls
from data import TestData
from http import HTTPStatus

@allure.step("Создание нового заказа и получение трек-номера")
def get_new_order_track():
    response = requests.post(Urls.URL_CREATE_ORDER, json=TestData.ORDER_DATA)
    return response.json()["track"]

@allure.title("Проверка получения заказа по его трек-номеру")
@allure.description("Создаем заказ, берем track и проверяем, что GET запрос возвращает 200 и данные заказа")
def test_get_order_by_track_success():
    # 1. Получаем трек
    track_number = get_new_order_track()
    
    # 2. Делаем запрос на получение заказа по треку (/api/v1/orders/track)
    response = requests.get(f"{Urls.URL_CREATE_ORDER}/track", params={"t": track_number})
    
    # 3. Проверка
    assert response.status_code == HTTPStatus.OK
    assert "order" in response.json() 

@allure.title("Проверка получения списка заказов")
@allure.description("Проверяем, что запрос на получение списка заказов возвращает 200 и в теле есть список")
def test_get_orders_list_returns_success():
    # Обращаемся к ручке GET /api/v1/orders
    response = requests.get(Urls.URL_CREATE_ORDER)
    
    # Проверяем код ответа
    assert response.status_code == HTTPStatus.OK
    
    # Проверяем, что в ответе есть ключ "orders" и это действительно список (list)
    assert "orders" in response.json()
    assert isinstance(response.json().get("orders"), list)


