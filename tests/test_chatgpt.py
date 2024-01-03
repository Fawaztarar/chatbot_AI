import pytest
from chatgpt import app, db, create_tables
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_chatbot_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Assistant' in response.get_data(as_text=True)


def test_handle_query(client):
    # Simulate a POST request to the endpoint
    response = client.post('/query', json={'query': 'What is the capital of France?'})
    
    # Check the response status code and body
    assert response.status_code == 200
    assert 'response' in response.json




# def test_handle_query_no_response(client):
#     test_query = {"query": ""}
#     response = client.post('/query', json=test_query)
#     assert response.status_code == 400

# def test_test_error_route(client):
#     response = client.get('/test_error')
#     assert response.status_code == 500
