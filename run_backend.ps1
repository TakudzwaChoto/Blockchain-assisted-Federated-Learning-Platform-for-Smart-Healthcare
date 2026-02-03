python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
