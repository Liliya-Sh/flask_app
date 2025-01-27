# flask_app
Flask приложение для кошелька.
Операции с кошельком:
 - создать;
 - посмотреть баланс по id(uuid);
 - снять или положить деньги.

Использавание SQLAlchemy БД: PostgreSQL.

_______________________________________________
# Запуск приложения.

Создать виртуальное окружение: python -m venv venv

Активировать виртуальное окружение(Windows): .venv\Scripts\activate

Скачать программу: git clone https://github.com/Liliya-Sh/flask_app.git

Установить зависимости: pip install-r requirements.txt

Запустить программу PyCharm: python run.py

Можно запустить имеющиеся тесты или в Postmane: pytest 
_______________________________________________
# Тестирование программы в Postmane.

1. Создаем кошелек [POST]: 
http://127.0.0.1:5000/api/v1/wallet_create

   {"balance": 0}

Результат:
{
    "message": "Кошелек создан",
    "wallet_id": str(wallet.id), 
    "balance": 0
}

Сохранем id для дальнейшей проверки.

2. Проверяем баланс созданного кошелька [GET]:
http://127.0.0.1:5000/api/v1/wallets/{wallet_id}/

Результат:
{
    "wallet_id": str(wallet.id),
    "balance": 0
}

3. Пополняем кошелек [POST]: 
http://127.0.0.1:5000/api/v1/wallets/{wallet_id}/operations

{
    "operationType": "deposit",
    "amount": 10
}

Результат:
{
    "message": "Баланс изменен",
    "new_balance": 10
}
4. Снимаем деньги с кошелька [POST]: 
http://127.0.0.1:5000/api/v1/wallets/{wallet_id}/operations

{
    "operationType": "withdraw",
    "amount": 10
}

Результат:
{
    "message": "Баланс изменен",
    "new_balance": 0
}
5. Если повторить операцию снятия:

Результат:
{
    "error": "Недостаточно средств для снятия."
}







