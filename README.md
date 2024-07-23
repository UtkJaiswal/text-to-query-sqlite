## Application to Fetch Data from a Natural Language Prompt to Fetching Data

### Features

- Provide a normal English text prompt.

- Get the desired results from the SQL database as described in the prompt.

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


