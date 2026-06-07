# ARANDU — Back (API)

API **FastAPI** do ARANDU — inteligência territorial hídrica nacional (27 UFs + visão Brasil).

| Ambiente | URL |
|----------|-----|
| **Produção** | https://arandu-back.onrender.com |
| **Swagger** | https://arandu-back.onrender.com/docs |
| **Health** | https://arandu-back.onrender.com/health |
| **Front** | https://aranduweb.vercel.app |
| **Repo front** | https://github.com/diegowalhernandes/arandu_front |

---

## Sobre o projeto

API REST que alimenta o dashboard com filtros territoriais, KPIs, mapa, gráficos e tabela analítica.

### Dados

> Os dados retornados **ainda são mockados (simulados)** via `DataService` (geração em memória com metadados reais de geografia em `app/core/brasil.py`).

> O **Supabase** (PostgreSQL + PostGIS) já está em uso como **banco em produção** — schema criado, credenciais em variáveis de ambiente no Render. A API **ainda não lê** as tabelas do Supabase; isso é o próximo passo.

Confirme em `/health`:

```json
{
  "status": "ok",
  "data_source": "mock",
  "database": "connected"
}
```

---

## Stack

| Tecnologia | Uso |
|------------|-----|
| FastAPI 0.115 | Framework |
| Uvicorn | Servidor ASGI |
| Pydantic 2 | Validação |
| Pandas / NumPy | Dados mock |
| SQLAlchemy 2 + psycopg2 | Conexão Postgres (preparada) |

---

## Endpoints

| Grupo | Rota |
|-------|------|
| Filtros | `GET /api/v1/filtros/opcoes` |
| | `GET /api/v1/filtros/municipios` |
| Dashboard | `GET /api/v1/dashboard/kpis` |
| | `GET /api/v1/dashboard/series/{indicador}` |
| | `GET /api/v1/dashboard/ranking` |
| | `GET /api/v1/dashboard/volume-bacia` |
| | `GET /api/v1/dashboard/vulnerabilidade` |
| | `GET /api/v1/dashboard/tabela` |
| | `GET /api/v1/dashboard/mapa/pontos` |
| | `GET /api/v1/dashboard/mapa/centro` |
| Sistema | `GET /health` |

Documentação interativa: `/docs`

---

## Desenvolvimento local

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## Variáveis de ambiente

Ver `.env.example`. Prefixo `ARANDU_` em todas.

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `ARANDU_USE_MOCK` | `true` | Dados simulados (desligar quando Supabase estiver integrado) |
| `ARANDU_DEBUG` | `true` | Modo debug |
| `ARANDU_CORS_ORIGINS` | `localhost:5173` | Origens permitidas (vírgula) |
| `ARANDU_DB_HOST` | `localhost` | Host Postgres / Supabase |
| `ARANDU_DB_PORT` | `5432` | Porta |
| `ARANDU_DB_NAME` | `arandu` | Nome do banco |
| `ARANDU_DB_USER` | `arandu` | Usuário |
| `ARANDU_DB_PASSWORD` | `arandu` | Senha |

---

## Produção (Render)

| Configuração | Valor |
|--------------|-------|
| **Runtime** | Python 3 ou Docker |
| **PYTHON_VERSION** | `3.12.8` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

Alternativa: runtime **Docker** (usa `Dockerfile` com `python:3.12-slim`).

### Variáveis no Render

| Variável | Valor recomendado |
|----------|-------------------|
| `ARANDU_USE_MOCK` | `true` |
| `ARANDU_DEBUG` | `false` |
| `ARANDU_CORS_ORIGINS` | `https://aranduweb.vercel.app` *(só se front chamar API direto)* |
| `ARANDU_DB_HOST` | `db.xxxxx.supabase.co` |
| `ARANDU_DB_PORT` | `5432` |
| `ARANDU_DB_NAME` | `postgres` |
| `ARANDU_DB_USER` | `postgres` |
| `ARANDU_DB_PASSWORD` | *(senha do Supabase)* |

> O front na Vercel usa proxy `/api` → Render, então CORS pode não ser necessário.

---

## Banco de dados (Supabase)

Schema PostGIS com tabelas: `estados`, `municipios`, `recursos_hidricos`, `estacoes`.

| Ambiente | Onde |
|----------|------|
| Produção | Supabase (PostgreSQL + PostGIS) |
| Desenvolvimento | Docker PostGIS local (pasta `bd/` no workspace ARANDU) |

Ordem de carga futura: `estados` → `municipios` → `recursos_hidricos` → `estacoes`.

Fontes planejadas: **IBGE** (malha municipal), **ANA/SNIRH** (estações hidrológicas), **INMET** (pluviometria).

---

## Próximos passos

- [ ] Ler dados reais do Supabase no `DataService`
- [ ] Script ETL — carga IBGE → Supabase
- [ ] Integração ANA (estações e medições)
- [ ] Job periódico de atualização
- [ ] `ARANDU_USE_MOCK=false` após integração
- [ ] Auth JWT
- [ ] Testes (pytest) e CI/CD

---

## Estrutura do repositório

```
app/
├── api/routes/         # dashboard, filtros
├── core/               # brasil.py, helpers
├── database/           # SQLAlchemy + check_connection
├── services/           # data_service.py (mock)
├── schemas/
├── config.py
└── main.py
data/geojson/           # GeoJSON (ainda não consumidos pela API)
```

---

ARANDU © 2026
