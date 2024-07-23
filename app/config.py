import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = 'database.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    conn.close()
    return tables

def get_metadata(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"PRAGMA table_info({table_name})"
    cursor.execute(query)
    columns = cursor.fetchall()
    metadata = []
    for column in columns:
        metadata.append(f"Field: {column['name']}, Type: {column['type']}, "
                        f"Null: {'YES' if column['notnull'] == 0 else 'NO'}, "
                        f"Key: {'PK' if column['pk'] == 1 else ''}, "
                        f"Default: {column['dflt_value']}")
    cursor.close()
    conn.close()
    return metadata

def generate_prompt(user_prompt, table_metadata):
    prompt = "Metadata:\n"
    for table, metadata in table_metadata.items():
        prompt += f"Table: {table}\n"
        prompt += f"{' | '.join(metadata)}\n\n"
    prompt += (
        f"You are given the metadata of the tables in the SQLite database with the above metadata.\n"
        f"You need to analyze this and write an SQL query in normal text (not even markdown) to answer the below natural language question. \n"
        f"Keep in mind this is for SQLite, so some MySQL-specific functions might not work.\n"
        f"Don't give any explanation, just write the query.\n"
        f"Question: {user_prompt}"
    )
    return prompt

def execute_sql_query(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(row) for row in results]
