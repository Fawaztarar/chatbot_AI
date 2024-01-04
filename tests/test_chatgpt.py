# test_chatgpt.py

#Run with: pytest tests/test_chatgpt.py
 
from flask.testing import FlaskClient
import pytest
from chatgpt import app, db


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


from unittest.mock import patch

def test_handle_query(client):
    # Mocking the OpenAI API call
    with patch('chatgpt.openai.Completion.create') as mock_openai:
        mock_openai.return_value = MockOpenAIResponse(choices=[MockChoice(text=' Paris')])

        # Define a sample query
        sample_query = {"query": "What is the capital of France?"}

        # Simulate a POST request to the /query route
        response = client.post('/query', json=sample_query)

        # Check that the response status code is 200 (OK)
        assert response.status_code == 200

        # Check the content of the response
        data = response.get_json()
        assert 'response' in data
        assert 'Paris' in data['response']  # Adjust based on expected response

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








