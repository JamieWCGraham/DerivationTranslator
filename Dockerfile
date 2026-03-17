# Derivation Translator — Streamlit app with OpenAI-backed explanations
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code (no .env — pass at run time)
COPY app.py llm.py parse.py prompts.py schemas.py utils.py ./

EXPOSE 8501

# Bind to 0.0.0.0 so the server is reachable outside the container
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
