# flask_app
Flask приложение для кошелька.
Операции с кошельком:
 - создать;
 - посмотреть баланс по id(uuid);
 - снять или положить деньги.

Использавание SQLAlchemy БД: PostgreSQL.

_______________________________________________
## Запуск приложения.

Создать виртуальное окружение: python -m venv venv

Активировать виртуальное окружение:

   (Windows): .venv\Scripts\activate

   (Linux): source venv/bin/activate

Скачать программу: git clone https://github.com/Liliya-Sh/flask_app.git

Установить зависимости: pip install -r requirements.txt

Перед запуском необходимо создать .env и .env.docker

Запустить программу PyCharm: python run.py

Можно запустить имеющиеся тесты: pytest 
или протестировать приложение в Postmane 
_______________________________________________
## Запуск приложения с помощью Docker

Это приложение можно запустить с помощью Docker.

### Предварительные требования

- Установленный [Docker](https://www.docker.com/get-started)

### Шаги для запуска
 
1. **Собрать Docker-образы**

   docker compose build
   
2. **Запустить приложение**

   docker compose up
   
   Это запустит приложение и все его зависимости. Можно открыть postman и перейти по адресу: 
   
   [POST] `http://localhost:8080/api/v1/wallet_create`

   Body: {
    "balance": 10
   }

   чтобы увидеть приложение в действии.

3. **Остановка приложения**

   `Ctrl + C` или docker compose down
_______________________________________________
## Тестирование программы в Postmane.

1. Создаем кошелек [POST]: 
   
   `http://127.0.0.1:5000/api/v1/wallet_create`

   {"balance": 0}


   Результат:
   {
    "message": "Кошелек создан",
    "wallet_id": str(wallet.id), 
    "balance": 0
   }

   Сохраняем id для дальнейшей проверки.

2. Проверяем баланс созданного кошелька [GET]:

   `http://127.0.0.1:5000/api/v1/wallets/{wallet_id}/`


   Результат:
   {
    "wallet_id": str(wallet.id),
    "balance": 0
   }

3. Пополняем кошелек [POST]: 
   `http://127.0.0.1:5000/api/v1/wallets/{wallet_id}/operations`

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
   `http://127.0.0.1:5000/api/v1/wallets/{wallet_id}/operations`

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
