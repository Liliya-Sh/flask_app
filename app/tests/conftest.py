import pytest
from app import create_app, db


@pytest.fixture(scope='module')
def test_app():
    # Создание приложения для тестирования
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin_db:password@127.0.0.1:5432/wallets_db'

    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture(scope='function')
def client(test_app):
    return test_app.test_client()

@pytest.fixture(autouse=True)
def session(test_app):
    """Фикстура для управления сессией базы данных."""
    with test_app.app_context():
        db.session.begin_nested()
        yield db.session
        db.session.rollback()
