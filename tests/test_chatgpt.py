# test_chatgpt.py

#Run with: pytest tests/test_chatgpt.py
 
from flask.testing import FlaskClient
import pytest
from chatgpt import app, db
from unittest.mock import patch


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

def test_chatbot_route(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Assistant' in response.get_data(as_text=True)






def test_handle_query(client):
    # Define a sample query
    sample_query = {"query": "What is the fee for makers bootcamp?"}

    # Simulate a POST request to the /query route
    response = client.post('/query', json=sample_query)

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check the content of the response
    data = response.get_json()
    assert 'response' in data

    # The response content might vary since it's coming from an actual API call
    # You may want to check if the response contains non-empty content
    # and possibly some expected keywords
    assert data['response']  # Check that response is not empty
    # If you expect specific content, you can assert for that as well, but be mindful
    # of the variability in the actual API response



class MockOpenAIResponse:
    def __init__(self, choices):
        self.choices = choices

class MockChoice:
    def __init__(self, text):
        self.text = text


def test_handle_query_no_response(client):
    # Mocking the OpenAI API call
    with patch('chatgpt.openai.Completion.create') as mock_openai:
        mock_openai.return_value = MockOpenAIResponse(choices=[])

        # Define a sample query
        sample_query = {"query": "What is the capital of France?"}

        # Simulate a POST request to the /query route
        response = client.post('/query', json=sample_query)

        # Check that the response status code is 400 (Bad Request)
        assert response.status_code == 400

        # Check the content of the response
        data = response.get_json()
        assert 'response' in data
        assert 'No response' in data['response']  # Adjust based on expected response


def test_handle_query_error(client):
    # Mocking the OpenAI API call
    with patch('chatgpt.openai.Completion.create') as mock_openai:
        mock_openai.side_effect = Exception('Something went wrong')

        # Define a sample query
        sample_query = {"query": "What is the capital of France?"}

        # Simulate a POST request to the /query route
        response = client.post('/query', json=sample_query)

        # Check that the response status code is 500 (Internal Server Error)
        assert response.status_code == 500

        # Check the content of the response
        data = response.get_json()
        assert 'error' in data
        assert 'Something went wrong' in data['error']  # Adjust based on expected response



def test_search(client):
    # Mocking the search function
    with patch('chatgpt.simple_search') as mock_search:
        mock_search.return_value = ['Paris', 'London', 'New York']

        # Define a sample query
        sample_query = {"query": "What is the capital of France?"}

        # Simulate a POST request to the /search route
        response = client.post('/search', json=sample_query)

        # Check that the response status code is 200 (OK)
        assert response.status_code == 200

        # Check the content of the response
        data = response.get_json()
        assert 'response' in data
        assert 'Paris' in data['response']  # Adjust based on expected response


def test_search_error(client):
    # Mocking the search function
    with patch('chatgpt.simple_search') as mock_search:
        mock_search.side_effect = Exception('Something went wrong')

        # Define a sample query
        sample_query = {"query": "What is the capital of France?"}

        # Simulate a POST request to the /search route
        response = client.post('/search', json=sample_query)

        # Check that the response status code is 500 (Internal Server Error)
        assert response.status_code == 500

        # Check the content of the response
        data = response.get_json()
        assert 'error' in data
        assert 'Something went wrong' in data['error']  # Adjust based on expected response

def test_store(client):
    # Mocking the store_data function
    with patch('chatgpt.store_data') as mock_store:
        mock_store.return_value = None

        # Define a sample query
        sample_query = {"query": "What is the capital of France?"}

        # Simulate a POST request to the /store route
        response = client.post('/store', json=sample_query)

        # Check that the response status code is 200 (OK)
        assert response.status_code == 200

        # Check the content of the response
        data = response.get_json()
        assert 'response' in data
        assert 'stored' in data['response']  # Adjust based on expected response


def test_store_error(client):
    # Mocking the store_data function
    with patch('chatgpt.store_data') as mock_store:
        mock_store.side_effect = Exception('Something went wrong')

        # Define a sample query
        sample_query = {"query": "What is the capital of France?"}

        # Simulate a POST request to the /store route
        response = client.post('/store', json=sample_query)

        # Check that the response status code is 500 (Internal Server Error)
        assert response.status_code == 500

        # Check the content of the response
        data = response.get_json()
        assert 'error' in data
        assert 'Something went wrong' in data['error']  # Adjust based on expected response

    








