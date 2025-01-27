import uuid

from flask import Blueprint, jsonify, request

from ..extensions import  db
from ..models.wallet import Wallet

wallet = Blueprint('wallet', __name__)


@wallet.route('/api/v1/wallet_create', methods=['POST'])
def create_wallet():
    """Создать кошелек с заданным балансом"""
    try:
        data = request.get_json(force=True)  # Используем force=True для обработки не JSON
    except Exception as e:
        return jsonify({"error": "Неверный формат данных. Убедитесь, что вы отправляете JSON."}), 400

    balance = data.get('balance')
    if balance is None:
        return jsonify({"error": "Укажите баланс кошелька."}), 400

    # Проверяем, что баланс является числом
    if not isinstance(balance, (int, float)):
        return jsonify({"error": "Баланс должен быть числом."}), 400

    wallet = Wallet(balance=balance)
    db.session.add(wallet)
    db.session.commit()
    return jsonify({"message": "Кошелек создан", "wallet_id": str(wallet.id), "balance": wallet.balance}), 201


@wallet.route("/api/v1/wallets/<string:wallet_id>/", methods=['GET'])
def view_balance(wallet_id):
    """Просмотреть баланс по uuid"""
    try:
        uuid_obj = uuid.UUID(wallet_id)
    except ValueError:
        return jsonify({"error": "Неверный формат wallet_id. Убедитесь, что это корректный UUID."}), 400
    wallet = db.session.get(Wallet, wallet_id)
    if not wallet:
        return jsonify({"error": "Кошелек не найден"}), 404

    return jsonify({"wallet_id": str(wallet.id), "balance": wallet.balance}), 200

@wallet.route("/api/v1/wallets/<string:wallet_id>/operations", methods=['POST'])
def wallet_operations(wallet_id):
    """Тип операции 'положить' или 'снять' деньги"""
    try:
        uuid_obj = uuid.UUID(wallet_id)
    except ValueError:
        return jsonify({"error": "Неверный формат wallet_id. Убедитесь, что это корректный UUID."}), 400
    data = request.get_json()

    if not data or 'operationType' not in data or 'amount' not in data:
        return jsonify({"error": "Invalid JSON format"}), 400

    operation = data['operationType'].lower()
    amount = data['amount']

    wallet = db.session.get(Wallet, wallet_id)
    if wallet is None:
        return jsonify({"error": "Кошелек не найден."}), 404

    current_balance = wallet.balance

    if operation == 'deposit':
        new_balance = current_balance + amount
    elif operation == 'withdraw':
        if current_balance >= amount:
            new_balance = current_balance - amount
        else:
            return jsonify({"error": "Недостаточно средств для снятия."}), 400
    else:
        return jsonify({"error": "Данная операция не доступна."}), 400

    wallet.balance = new_balance
    db.session.commit()

    return jsonify({"message": "Баланс изменен", "new_balance": new_balance}), 200
