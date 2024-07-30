from flask import request, jsonify, current_app
from dotenv import load_dotenv
from services.ai_service import generate_sql_query
from .config import *


@current_app.route('/generate-and-execute-sql', methods=['POST'])
def generate_and_execute_sql():
    try:
        data = request.json
        user_prompt = data['prompt']

        combined_prompt = generate_prompt(user_prompt)

        documents = current_app.config['DOCUMENTS']
        
        sql_query = generate_sql_query(documents, combined_prompt)
        
        results = execute_sql_query(str(sql_query))
        
        response = jsonify({
            'results': results
        })
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500