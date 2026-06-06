"""Utilitários do backend."""

from __future__ import annotations

from typing import Any

import pandas as pd


def filter_dataframe(df: pd.DataFrame, **filters: Any) -> pd.DataFrame:
    """Aplica filtros territoriais a um DataFrame."""
    result = df.copy()

    estado = filters.get("estado")
    if estado and estado != "BR" and "estado" in result.columns:
        result = result[result["estado"] == estado]

    if municipio := filters.get("municipio"):
        if municipio != "todos" and "municipio_id" in result.columns:
            result = result[result["municipio_id"] == municipio]
        elif municipio != "todos" and "id" in result.columns and "nome" in result.columns:
            result = result[result["id"] == municipio]

    if regiao := filters.get("regiao"):
        if regiao != "todos" and "regiao" in result.columns:
            result = result[result["regiao"] == regiao]

    if bacia := filters.get("bacia"):
        if bacia != "todos" and "bacia" in result.columns:
            result = result[result["bacia"] == bacia]

    if tipo := filters.get("tipo_recurso"):
        if tipo != "todos" and "tipo" in result.columns:
            result = result[result["tipo"] == tipo]

    if criticidade := filters.get("criticidade"):
        if criticidade != "todas" and "status" in result.columns:
            result = result[result["status"] == criticidade]

    return result


def df_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Converte DataFrame para registros JSON-serializáveis."""
    if df.empty:
        return []
    out = df.copy()
    for col in out.select_dtypes(include=["datetime", "datetimetz"]).columns:
        out[col] = out[col].astype(str)
    return out.where(pd.notna(out), None).to_dict(orient="records")
