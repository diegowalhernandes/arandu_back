"""Rotas de metadados e filtros."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from app.core.constants import CRITICIDADE, MAP_LAYERS, PERIODOS, REGIOES_BRASIL, TIPOS_RECURSO
from app.services.data_service import get_data_service
from app.core.helpers import df_to_records

router = APIRouter(prefix="/filtros", tags=["Filtros"])


@router.get("/opcoes")
def get_opcoes(estado: str = Query("BR")) -> dict[str, Any]:
    """Retorna todas as opções de filtros."""
    svc = get_data_service()
    kw = {"estado": estado} if estado != "BR" else {}
    municipios = svc.get_municipios(**kw)
    mun_opts = [{"label": "Todos", "value": "todos"}]
    for _, row in municipios.drop_duplicates("nome").iterrows():
        mun_opts.append({"label": f"{row['nome']} ({row['estado']})", "value": row["id"]})

    bacias = municipios["bacia"].drop_duplicates().tolist()
    bacia_opts = [{"label": "Todas", "value": "todos"}]
    for b in bacias:
        bacia_opts.append({"label": b.replace("_", " ").title(), "value": b})

    return {
        "estados": svc.get_estados(),
        "municipios": mun_opts,
        "regioes": [{"label": "Todas", "value": "todos"}, *REGIOES_BRASIL],
        "bacias": bacia_opts,
        "tipos_recurso": TIPOS_RECURSO,
        "criticidade": CRITICIDADE,
        "periodos": PERIODOS,
        "camadas_mapa": MAP_LAYERS,
    }


@router.get("/municipios")
def get_municipios(estado: str = Query("BR")) -> list[dict[str, Any]]:
    """Lista municípios filtrados por estado."""
    kw = {"estado": estado} if estado != "BR" else {}
    return df_to_records(get_data_service().get_municipios(**kw))
