from flask import Flask
from flask_cors import CORS
from .config import initialize_app_data
from services.ai_service import initialize_ai_service

def create_app():
    app = Flask(__name__)
    CORS(app)

    with app.app_context():
        tables, table_metadata, documents = initialize_app_data()

        initialize_ai_service(documents)

        from . import routes
        
        app.config['TABLES'] = tables
        app.config['TABLE_METADATA'] = table_metadata
        app.config['DOCUMENTS'] = documents

    return app
