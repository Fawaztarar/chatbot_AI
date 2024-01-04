# test__db_models.py
import pytest
from lib.db_models import ExtractedData
from chatgpt import *


import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from chatgpt import db  # Adjust import as necessary
import os
import openai
from flask import Flask
from flask.testing import FlaskClient

class Config:
    # Assuming you have a Config class similar to your production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    # You may need to add other configurations that are essential for your tests

@pytest.fixture
def test_app():
    """Create and configure a new app instance for each test."""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()



def test_create_tables(test_app):
    """Test the create_tables function."""
    with test_app.app_context():
        create_tables(test_app)
        assert ExtractedData.query.first() is None
        # Add assertions to check if tables are created correctly

def test_query_data(test_app):
    """Test the query_data function."""
    with test_app.app_context():
        # Add assertions to check if data is queried correctly
        results = query_data('test')
        assert results == []
        store_data('web', 'Example content')
        results = query_data('Example')
        assert len(results) == 1
        assert results[0].source == 'web'
        assert results[0].content == 'Example content'




def test_store_data(test_app):
    """Test the store_data function."""
    with test_app.app_context():
        store_data('web', 'Example content')
        # Add assertions to check if data is stored correctly
        stored_data = ExtractedData.query.first()
        assert stored_data is not None
        assert stored_data.source == 'web'
        assert stored_data.content == 'Example content'

# ...




# ... (Other parts of the file, like Config and test_app fixture)

def test_extracted_data_model(test_app):
    """Test the ExtractedData model."""
    with test_app.app_context():
        # Create a new record in the database
        new_data = ExtractedData(source='web', content='Example content')
        db.session.add(new_data)
        db.session.commit()

        # Retrieve the record from the database
        stored_data = ExtractedData.query.first()

        # Compare the data
        assert stored_data is not None
        assert stored_data.source == 'web'
        assert stored_data.content == 'Example content'





