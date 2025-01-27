def test_create_wallet(client):
    """Тестируем функцию создания нового кошелька"""
    response = client.post("/api/v1/wallet_create", json={"balance": 100})
    assert response.status_code == 201
    assert "Кошелек создан" in response.get_json()["message"]

def test_create_wallet_balance_none(client):
    """Тестируем функцию создания нового кошелька, без указания баланса"""
    response = client.post("/api/v1/wallet_create", json={"balance": None})
    assert response.status_code == 400
    assert "Укажите баланс кошелька." in response.get_json()["error"]


def test_view_balance(client):
    """Тестируем функцию просмотра баланса"""
    response = client.post("/api/v1/wallet_create", json={"balance": 100})
    wallet_id = response.get_json()["wallet_id"]

    response = client.get(f"/api/v1/wallets/{wallet_id}/")
    assert response.status_code == 200
    assert response.get_json() == {"wallet_id": wallet_id, "balance": 100}


def test_view_balance_id_none(client):
    """Тестируем функцию просмотра баланса с несуществующим wallet_id"""
    # Используем недопустимый UUID
    invalid_wallet_id = "00000000-0000-0000-0000-000000000000"  # Пример недопустимого UUID

    response = client.get(f"/api/v1/wallets/{invalid_wallet_id}/")
    assert response.status_code == 404
    assert "Кошелек не найден" in response.get_json()["error"]

def test_wallet_operations_deposit(client):
    """Тестируем функцию wallet_operations(проверяем операцию 'положить' деньги)"""
    wallet_response = client.post("/api/v1/wallet_create", json={"balance": 0})
    wallet_id = wallet_response.get_json()["wallet_id"]

    response = client.post(f"/api/v1/wallets/{wallet_id}/operations",
                                    json={"operationType": "deposit", "amount": 1000})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Баланс изменен", "new_balance": 1000}

def test_wallet_operations_withdraw(client):
    """Тестируем функцию wallet_operations(проверяем операцию 'снять' деньги)"""
    wallet_response = client.post("/api/v1/wallet_create", json={"balance": 1000})
    wallet_id = wallet_response.get_json()["wallet_id"]

    response = client.post(f"/api/v1/wallets/{wallet_id}/operations",
                                    json={"operationType": "withdraw", "amount": 500})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Баланс изменен", "new_balance": 500}

def test_wallet_operations_withdraw_insufficient_funds(client):
    """Тестируем функцию wallet_operations(недостаточно средств для снятия)"""
    wallet_response = client.post("/api/v1/wallet_create", json={"balance": 100})
    wallet_id = wallet_response.get_json()["wallet_id"]

    response = client.post(f"/api/v1/wallets/{wallet_id}/operations",
                                    json={"operationType": "withdraw", "amount": 200})
    assert response.status_code == 400
    assert "Недостаточно средств для снятия." in response.get_json()["error"]


def test_wallet_operations_invalid_operation(client):
    """Тестируем функцию wallet_operations(недопустимая операция)"""
    wallet_response = client.post("/api/v1/wallet_create", json={"balance": 100})
    wallet_id = wallet_response.get_json()["wallet_id"]

    response = client.post(f"/api/v1/wallets/{wallet_id}/operations",
                                    json={"operationType": "", "amount": 100})
    assert response.status_code == 400
    assert "Данная операция не доступна." in response.get_json()["error"]
