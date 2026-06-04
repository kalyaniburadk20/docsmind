# DocsMind Backend

FastAPI backend for the DocsMind RAG agent.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

API available at `http://localhost:8000`.
Swagger docs at `http://localhost:8000/docs`.