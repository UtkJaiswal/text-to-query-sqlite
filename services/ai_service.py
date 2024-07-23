import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()


genai.configure(api_key=os.getenv('GENAI_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-flash')

def generate_sql_query(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()
