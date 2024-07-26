from flask import Flask, request, jsonify, current_app
from dotenv import load_dotenv
from services.ai_service import generate_sql_query
from .config import *

load_dotenv()

@current_app.route('/generate-and-execute-sql', methods=['POST'])
def generate_and_execute_sql():
    try:

        data = request.json
        user_prompt = data['prompt']


        tables = get_tables()
        table_metadata = {}

        for table in tables:
            table_metadata[table] = get_metadata(table)


        documents = textToDocument(table_metadata)

        combined_prompt = generate_prompt(user_prompt, table_metadata)
        
        sql_query = generate_sql_query(documents, combined_prompt)

        
        results = execute_sql_query(str(sql_query))
        
        response = jsonify({
            'results': results
        })
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500