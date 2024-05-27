import pytest
from unittest.mock import patch
from app import app, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
    with app.test_client() as client:
        with app.app_context():
            # Create all tables in the in-memory SQLite database
            from app import db
            db.create_all()
        yield client

def test_users_list(client):
    with app.app_context():
    # Mock the query.all() method to return a known result
        with patch('app.User.query') as mock_query:
            mock_query.all.return_value = [
                User(id=1, username='testuser1', email='test1@example.com', password='password1'),
                User(id=2, username='testuser2', email='test2@example.com', password='password2')
            ]

            response = client.get('/users')
            assert response.status_code == 200

            json_data = response.get_json()
            assert json_data['code'] == 200
            assert json_data['message'] == "datos solicitados exitosamente."
            assert len(json_data['data']) == 2
            assert json_data['data'][0]['username'] == 'testuser1'
            assert json_data['data'][1]['username'] == 'testuser2'
