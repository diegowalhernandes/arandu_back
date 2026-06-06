# ARANDU — Back (API)

FastAPI — inteligência territorial hídrica nacional.

## Subir apenas a API

```bash
cd back
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Variáveis

Ver `.env.example`. Com `ARANDU_USE_MOCK=true` (padrão), a API funciona sem o banco.
