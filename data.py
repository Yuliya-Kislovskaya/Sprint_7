class TestData:
    CORRECT_LOGIN = "Violet_2024" 
    CORRECT_PASSWORD = "12345"
    CORRECT_NAME = "Violetta"

    # Данные для создания курьера (ошибка 400)
    MISSING_FIELDS_DATA = [
        {"password": "123", "firstName": "Violetta"}, # Без логина
        {"login": "Violet_2024", "firstName": "Violetta"}, # Без пароля
        {"firstName": "Violetta"} # Без обоих
    ]

    # Данные для логина курьера (пустые поля)
    LOGIN_MISSING_FIELDS = [
        {'login': '', 'password': "some_password"},
        {'login': "some_login", 'password': ''},
    ]

    ORDER_DATA = {
        "firstName": "Nadya",
        "lastName": "Kovaleva",
        "address": "Moscow, Lenina street",
        "metroStation": 4, 
        "phone": "+7 900 555 55 55",
        "rentTime": 5,
        "deliveryDate": "2026-03-22",
        "comment": "Live is life",
        "color": [] 
    }
    ORDER_COLORS = [
        ["BLACK"], 
        ["GREY"], 
        ["BLACK", "GREY"], 
        []
    ]

    
    MESSAGE_CONFLICT = {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}
    MESSAGE_BAD_REQUEST = {"code": 400, "message": "Недостаточно данных для создания учетной записи"}
    MESSAGE_NOT_FOUND = {"code": 404, "message": "Учетная запись не найдена"}
    MESSAGE_LOGIN_BAD_REQUEST = {"code": 400, "message": "Недостаточно данных для входа"}

