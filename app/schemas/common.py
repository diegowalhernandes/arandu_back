"""Schemas Pydantic compartilhados."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    """Parâmetros de filtro territorial."""

    estado: str = Field(default="BR", description="UF ou BR para nacional")
    municipio: str = Field(default="todos")
    regiao: str = Field(default="todos")
    bacia: str = Field(default="todos")
    tipo_recurso: str = Field(default="todos")
    criticidade: str = Field(default="todas")
    periodo: str = Field(default="30d")

    def to_kwargs(self) -> dict[str, Any]:
        """Converte para kwargs do serviço de dados."""
        return {
            "estado": self.estado if self.estado != "BR" else None,
            **{k: v for k, v in {
                "municipio": self.municipio,
                "regiao": self.regiao,
                "bacia": self.bacia,
                "tipo_recurso": self.tipo_recurso,
                "criticidade": self.criticidade,
            }.items()},
        }


class HealthResponse(BaseModel):
    """Resposta de health check."""

    status: str
    app: str
    version: str
