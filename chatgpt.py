import os
import openai
import requests
from flask import Flask, request, jsonify, render_template
import json
from PyPDF2 import PdfReader
import pdfplumber
from bs4 import BeautifulSoup
from lib.config import Config
from lib.db_models import db, store_data, query_data, create_tables
from lib.search import simple_search

app = Flask(__name__)
app.config.from_object(Config)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///chatbot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def initialize_app():
    with app.app_context():
        create_tables(app)
    openai.api_key = app.config['OPENAI_API_KEY']

# Routes
@app.route('/')
def chatbot():
    return render_template('ai_chatbot.html')




@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    query = data['query']

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Q: {query}\nA:",
            max_tokens=150
        )
        if response:
            answer = response.choices[0].text.strip() if response.choices else 'No response'
            return jsonify({'response': answer})
        else:
            return jsonify({'response': 'No response from the model'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/test_error')
def test_error():
    raise Exception('Test exception')

if __name__ == '__main__':
    initialize_app()
    app.run(debug=False, port=5001)









