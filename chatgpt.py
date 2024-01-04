import os
import openai
import requests
from flask import Flask, request, jsonify, render_template
import json
from pypdf import PdfReader
import pdfplumber
from lib.config import Config
from lib.db_models import db, store_data, query_data, create_tables
from lib.search import simple_search
import traceback


app = Flask(__name__)
app.config.from_object(Config)
app.config['DEBUG'] = True

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
    try:
        # Get the JSON data from the request
        data = request.get_json()
        query = data['query']

        # Call OpenAI's Completion API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Q: {query}\nA:",
            max_tokens=150
        )

        # Check if a valid response was received
        if response and response.choices:
            answer = response.choices[0].text.strip()
            return jsonify({'response': answer})
        else:
            return jsonify({'response': 'No response from the model'}), 400

    except Exception as e:
        # Return a JSON response with the error message and a 500 status code
        return jsonify({'error': str(e)}), 500

    

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data['query']
    try:
        results = simple_search(query)
        return jsonify({'response': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/store', methods=['POST'])
def store():
    data = request.get_json()
    query = data['query']
    try:
        store_data(query)
        return jsonify({'response': 'Data stored successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    














if __name__ == '__main__':
    initialize_app()
    app.run(debug=True, port=5001)









