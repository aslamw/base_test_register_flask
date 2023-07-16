# test_auth.py

import pytest
from your_app import create_app
from your_app.models import User

@pytest.fixture
def app():
    """Fixture para criar a aplicação Flask para os testes."""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Fixture para criar um cliente de teste para a aplicação."""
    return app.test_client()

@pytest.fixture
def db(app):
    """Fixture para configurar o banco de dados para os testes."""
    with app.app_context():
        # Criar tabelas do banco de dados
        db.create_all()

        # Inserir usuário de teste
        user = User(username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()

        yield db

        # Limpar tabelas do banco de dados após os testes
        db.drop_all()

def test_login(client, db):
    """Teste de login com um usuário válido."""
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert b'Login successful' in response.data

def test_login_invalid_user(client, db):
    """Teste de login com um usuário inválido."""
    response = client.post('/login', data={'username': 'invaliduser', 'password': 'invalidpassword'})
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_register(client, db):
    """Teste de registro de um novo usuário."""
    response = client.post('/register', data={'username': 'newuser', 'password': 'newpassword'})
    assert response.status_code == 200
    assert b'Registration successful' in response.data
