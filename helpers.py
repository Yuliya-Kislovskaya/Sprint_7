import requests
import random
import string
import allure
from urls import Urls

def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    with allure.step('Запрос на создание нового курьера в хелпере'):
        response = requests.post(Urls.URL_CREATE_COURIER, json=payload)

    if response.status_code == 201:
        return [login, password, first_name]
    
    return [] 

