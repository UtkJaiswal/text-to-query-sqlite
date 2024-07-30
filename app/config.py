import sqlite3
from llama_index.core import Document
import pickle, os

DATABASE_PATH = 'database.sqlite'
PICKLE_FILE = 'app_data.pickle'

def get_db_connection():

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    except Exception as e:
        raise RuntimeError(f"Error connecting to database: {e}")


def get_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        return tables
    
    except Exception as e:
        return RuntimeError(f"Error fetching tables: {e}")
    
    finally:
        cursor.close()
        conn.close()
    

def get_metadata(table_name):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        query = f"PRAGMA table_info({table_name})"
        cursor.execute(query)
        columns = cursor.fetchall()
        metadata = []
        for column in columns:
            metadata.append(f"Field: {column['name']}, Type: {column['type']}, "
                            f"Null: {'YES' if column['notnull'] == 0 else 'NO'}, "
                            f"Key: {'PK' if column['pk'] == 1 else ''}, "
                            f"Default: {column['dflt_value']}")
        return metadata
    
    except Exception as e:
        raise RuntimeError(f"Error fetching metadata for table {table_name}: {e}")
    
    finally:
        cursor.close()
        conn.close()
    

def textToDocument(table_metadata):
    documents = []
    try:
        for table_name, fields in table_metadata.items():
            table_info = f"Table name: {table_name}\n"
            table_info += "\n".join(fields)
            documents.append(Document(text=table_info))

        return documents
    
    except Exception as e:
        raise RuntimeError(f"Error converting text to document: {e}")


def generate_prompt(user_prompt):

    try:
        prompt = "Metadata:\n"
        prompt += (
            f"You are given the metadata of the tables in the SQLite database with the above metadata.\n"
            f"You need to analyze this and write an SQL query in normal text (not even markdown) to answer the below natural language question. \n"
            f"Keep in mind this is for SQLite, so some MySQL-specific functions might not work.\n"
            f"Don't give any explanation, just write the query.\n"
            f"Question: {user_prompt}"
        )
        return prompt
    
    except Exception as e:
        raise RuntimeError(f"Error generating prompt: {e}")


def execute_sql_query(query):

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return [dict(row) for row in results]
    
    except Exception as e:
        raise RuntimeError(f"Error executing query: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def initialize_app_data():
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
    
    return tables, table_metadata, documents