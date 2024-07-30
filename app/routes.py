from flask import request, jsonify, current_app
from dotenv import load_dotenv
from services.ai_service import generate_sql_query
from .config import *
import pickle, os


tables = []
table_metadata = {}
documents = None

PICKLE_FILE = 'app_data.pickle'

def initialize_app():
    global tables, table_metadata, documents
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as f:
            data = pickle.load(f)
            tables = data['tables']
            table_metadata = data['table_metadata']
            documents = data['documents']
    else:
        tables = get_tables()
        table_metadata = {}
        for table in tables:
            table_metadata[table] = get_metadata(table)
        documents = textToDocument(table_metadata)
        
        
        with open(PICKLE_FILE, 'wb') as f:
            pickle.dump({
                'tables': tables,
                'table_metadata': table_metadata,
                'documents': documents
            }, f)


@current_app.route('/generate-and-execute-sql', methods=['POST'])
def generate_and_execute_sql():
    try:
        data = request.json
        user_prompt = data['prompt']

        combined_prompt = generate_prompt(user_prompt, table_metadata)
        
        sql_query = generate_sql_query(documents, combined_prompt)
        
        results = execute_sql_query(str(sql_query))
        
        response = jsonify({
            'results': results
        })
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500