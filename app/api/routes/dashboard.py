"""Rotas do dashboard."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from app.schemas.common import FilterParams
from app.services.data_service import get_data_service
from app.core.helpers import df_to_records

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def _filters(
    estado: str = "BR",
    municipio: str = "todos",
    regiao: str = "todos",
    bacia: str = "todos",
    tipo_recurso: str = "todos",
    criticidade: str = "todas",
    periodo: str = "30d",
) -> dict[str, Any]:
    return FilterParams(
        estado=estado, municipio=municipio, regiao=regiao,
        bacia=bacia, tipo_recurso=tipo_recurso, criticidade=criticidade, periodo=periodo,
    ).to_kwargs()


@router.get("/kpis")
def get_kpis(
    estado: str = Query("BR"),
    municipio: str = Query("todos"),
    regiao: str = Query("todos"),
    bacia: str = Query("todos"),
    tipo_recurso: str = Query("todos"),
    criticidade: str = Query("todas"),
) -> dict[str, Any]:
    """Indicadores KPI do dashboard."""
    svc = get_data_service()
    kw = _filters(estado, municipio, regiao, bacia, tipo_recurso, criticidade)
    if kw.get("estado") is None:
        kw.pop("estado", None)
    return svc.get_kpis(**{k: v for k, v in kw.items() if v and v not in ("todos", "todas")})


@router.get("/series/{indicador}")
def get_series(
    indicador: str,
    periodo: str = Query("30d"),
    estado: str = Query("BR"),
) -> list[dict[str, Any]]:
    """Série temporal."""
    return df_to_records(get_data_service().get_serie_temporal(indicador, periodo))


@router.get("/ranking")
def get_ranking(
    estado: str = Query("BR"),
    regiao: str = Query("todos"),
    criticidade: str = Query("todas"),
) -> list[dict[str, Any]]:
    """Ranking de municípios críticos."""
    kw: dict[str, Any] = {}
    if estado != "BR":
        kw["estado"] = estado
    if regiao != "todos":
        kw["regiao"] = regiao
    if criticidade != "todas":
        kw["criticidade"] = criticidade
    return df_to_records(get_data_service().get_ranking_municipios(**kw))


@router.get("/volume-bacia")
def get_volume_bacia(estado: str = Query("BR")) -> list[dict[str, Any]]:
    """Volume por bacia hidrográfica."""
    kw = {"estado": estado} if estado != "BR" else {}
    return df_to_records(get_data_service().get_volume_por_bacia(**kw))


@router.get("/vulnerabilidade")
def get_vulnerabilidade(estado: str = Query("BR")) -> list[dict[str, Any]]:
    """Vulnerabilidade por região."""
    kw = {"estado": estado} if estado != "BR" else {}
    return df_to_records(get_data_service().get_vulnerabilidade_regiao(**kw))


@router.get("/tabela")
def get_tabela(
    estado: str = Query("BR"),
    municipio: str = Query("todos"),
    regiao: str = Query("todos"),
    bacia: str = Query("todos"),
    tipo_recurso: str = Query("todos"),
    criticidade: str = Query("todas"),
    busca: str = Query(""),
) -> list[dict[str, Any]]:
    """Tabela analítica de recursos."""
    kw: dict[str, Any] = {}
    if estado != "BR":
        kw["estado"] = estado
    for key, val, skip in [
        ("municipio", municipio, "todos"),
        ("regiao", regiao, "todos"),
        ("bacia", bacia, "todos"),
        ("tipo_recurso", tipo_recurso, "todos"),
        ("criticidade", criticidade, "todas"),
    ]:
        if val != skip:
            kw[key] = val
    df = get_data_service().get_tabela(**kw)
    if busca:
        mask = df.apply(
            lambda row: row.astype(str).str.contains(busca, case=False, na=False).any(),
            axis=1,
        )
        df = df[mask]
    return df_to_records(df)


@router.get("/mapa/pontos")
def get_mapa_pontos(
    estado: str = Query("BR"),
    layers: str = Query("municipios,reservatorios,estacoes_hidro"),
    regiao: str = Query("todos"),
    criticidade: str = Query("todas"),
) -> list[dict[str, Any]]:
    """Pontos georreferenciados para o mapa."""
    kw: dict[str, Any] = {}
    if estado != "BR":
        kw["estado"] = estado
    if regiao != "todos":
        kw["regiao"] = regiao
    if criticidade != "todas":
        kw["criticidade"] = criticidade
    layer_list = [l.strip() for l in layers.split(",") if l.strip()]
    return get_data_service().get_map_points(layer_list, **kw)


@router.get("/mapa/centro")
def get_mapa_centro(estado: str = Query("BR")) -> dict[str, Any]:
    """Centro e zoom do mapa."""
    return get_data_service().get_map_center(estado)
