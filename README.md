## Application to Fetch Data from a Natural Language Prompt to Fetching Data

### Features

- Provide a normal English text prompt.

- Get the desired results from the SQLite database as described in the prompt.

- Database used is `sqlite` in the root directory of the folder named `database.sqlite`

### Installations

- Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

- Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

- Install the dependencies from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

### Project Setup

- Create a `.env` file in the root directory.

- Add the following details:

    ```
    GENAI_API_KEY=api_key_for_Gemini_app
    ```

### Run the Project

```bash
python run.py
```

### Data Engineering Process: Raw Data to API-Ready

1. **Database Connection Setup**
   - Implemented `get_db_connection()` function
   - Used `SQLite` for database interaction

2. **Schema Exploration**
   - Created `get_tables()` function to retrieve all table names
   - Implemented error handling for table fetching

3. **Metadata Extraction**
   - Developed `get_metadata(table_name)` function
   - Extracted detailed column information for each table
   - Included field name, data type, null constraint, primary key, and default value

4. **Data Structure Conversion**
   - Created `textToDocument(table_metadata)` function
   - Converted table metadata into Document objects from LlamaIndex
   - Utilized `llama_index.core.Document` for structured representation of metadata

5. **LlamaIndex Integration**
   - Imported necessary components from LlamaIndex
   - Used LlamaIndex's Document class to create indexable content
   - Prepared data for potential indexing and retrieval operations
   - Utilized LlamaIndex's capabilities for advanced query understanding
   - Potentially used LlamaIndex for query expansion or semantic search over metadata

6. **Query Generation**
   - Implemented `generate_prompt(user_prompt, table_metadata)` function
   - Constructed a comprehensive prompt including:
     - Table metadata
     - Context for SQL query generation
     - User's natural language question

7. **Query Execution**
   - Developed `execute_sql_query(query)` function
   - Executed the generated SQL query against the database
   - Converted results to a list of dictionaries for easy API consumption


8. **API Integration**
   - Exposed the processed data and query execution capability through an API


### API Functionality

#### Endpoint: `/generate-and-execute-sql`

**Method:** POST

**Functinality**

1. **Input Processing**
    - Accepts a JSON payload with a 'prompt' field containing the user's natural language query

2. **Response**
    - Executes the generated SQL query by LLM against the database to fetch the results and returns the response


### Key challenges faced

1. **Model Selection**
   - Challenge: Finding a suitable, cost-effective model for natural language processing
   - Solution: Chose Gemini model due to its effectiveness and free availability
   - Consideration: Balanced performance requirements with budget constraints

2. **Integration of LlamaIndex**
   - Challenge: Effectively incorporating LlamaIndex into the data processing pipeline
   - Solution: Utilized LlamaIndex's Document class for structured metadata representation
   - Benefit: Enhanced capability for potential advanced querying and indexing