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
    sample_query = "What is the capital of France?"
    response = client.post('/query', json={'query': sample_query})
    response_data = response.data.decode('utf-8')  # Decode the response data
    print(response_data)
    assert response.status_code == 200




# def test_handle_query_no_response(client):
#     test_query = {"query": ""}
#     response = client.post('/query', json=test_query)
#     assert response.status_code == 400

# def test_test_error_route(client):
#     response = client.get('/test_error')
#     assert response.status_code == 500
