import os
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import ServiceContext, Settings, VectorStoreIndex


load_dotenv()

gemini_api_key = os.getenv('GENAI_API_KEY')

def generate_sql_query(documents, combined_prompt):

    if gemini_api_key is None:
        raise ValueError("Gemini API key is not set")
    if not documents:
        raise ValueError("Documents list is empty")
    if not combined_prompt:
        raise ValueError("Prompt is empty")

    try:

        
        llm = Gemini(
            model=f"models/gemini-1.5-flash",
            api_key=gemini_api_key
        )

        
        embed_model = GeminiEmbedding(
            model_name=f"models/embedding-001",
            api_key=gemini_api_key
        )

       
        Settings.llm = llm
        Settings.embed_model = embed_model
        ServiceContext.chunk_size = 1024

      
        service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model
        )

        
        index = VectorStoreIndex.from_documents(
            documents,
            service_context=service_context
        )

        
        query_engine = index.as_query_engine()
        response = query_engine.query(combined_prompt)

        return response

    except Exception as e:
        raise RuntimeError(f"An error occurred during query execution: {e}")
