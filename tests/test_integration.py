import pytest
from unittest.mock import patch
from chatgpt import * # Import your Flask app creation function
from unittest.mock import patch, MagicMock

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

openai_response = MagicMock()
openai_response.choices = [MagicMock(text='AI response')]

scrapy_response = {'data': 'scraped data'}
pdf_response = 'text from pdf'
text_response = 'text data'



def test_complete_workflow(client):
    with patch('yourapplication.openai.Completion.create', return_value=openai_response) as mock_openai, \
         patch('yourapplication.scrapy_function', return_value=scrapy_response) as mock_scrapy, \
         patch('yourapplication.pdf_reader_function', return_value=pdf_response) as mock_pdf_reader, \
         patch('yourapplication.text_reader_function', return_value=text_response) as mock_text_reader:

        # Step 1: Simulate user query via chatbot
        user_query = {"query": "Extract data from this URL"}
        response = client.post('/chatbot', json=user_query)
        assert response.status_code == 200
        assert 'AI response' in response.get_json()['response']

        # Verify if Scrapy was called for web scraping
        mock_scrapy.assert_called_once()

        # Step 2: Simulate a query requiring PDF reading
        user_query = {"query": "Read this PDF"}
        response = client.post('/chatbot', json=user_query)
        assert response.status_code == 200
        assert 'text from pdf' in response.get_json()['response']

        # Verify if PDF reader was called
        mock_pdf_reader.assert_called_once()

        # Step 3: Simulate a query for text reading
        user_query = {"query": "Process this text"}
        response = client.post('/chatbot', json=user_query)
        assert response.status_code == 200
        assert 'text data' in response.get_json()['response']

        # Verify if text reader was called
        mock_text_reader.assert_called_once()
