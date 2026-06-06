"""Constantes nacionais da plataforma ARANDU."""

from __future__ import annotations

from typing import Final

APP_NAME: Final[str] = "ARANDU"
APP_SLOGAN: Final[str] = (
    "Plataforma Brasileira de Monitoramento e Inteligência Territorial"
)

# Centro geográfico do Brasil
BRASIL_CENTER: Final[tuple[float, float]] = (-14.2350, -51.9253)
BRASIL_ZOOM: Final[int] = 4

STATUS_LABELS: Final[dict[str, str]] = {
    "normal": "Normal",
    "atencao": "Atenção",
    "critico": "Crítico",
    "sem_dados": "Sem dados",
}

STATUS_COLORS: Final[dict[str, str]] = {
    "normal": "#10B981",
    "atencao": "#F59E0B",
    "critico": "#EF4444",
    "sem_dados": "#94A3B8",
}

TIPOS_RECURSO: Final[list[dict[str, str]]] = [
    {"label": "Todos", "value": "todos"},
    {"label": "Reservatórios", "value": "reservatorio"},
    {"label": "Rios", "value": "rio"},
    {"label": "Nascentes", "value": "nascente"},
    {"label": "Represas", "value": "represa"},
    {"label": "Estações Hidrológicas", "value": "estacao_hidro"},
    {"label": "Estações Pluviométricas", "value": "estacao_pluvio"},
]

CRITICIDADE: Final[list[dict[str, str]]] = [
    {"label": "Todas", "value": "todas"},
    {"label": "Normal", "value": "normal"},
    {"label": "Atenção", "value": "atencao"},
    {"label": "Crítico", "value": "critico"},
]

PERIODOS: Final[list[dict[str, str]]] = [
    {"label": "Últimos 7 dias", "value": "7d"},
    {"label": "Últimos 30 dias", "value": "30d"},
    {"label": "Últimos 90 dias", "value": "90d"},
    {"label": "Último ano", "value": "1y"},
    {"label": "Histórico completo", "value": "all"},
]

MAP_LAYERS: Final[list[dict[str, str]]] = [
    {"label": "Municípios", "value": "municipios"},
    {"label": "Rios", "value": "rios"},
    {"label": "Reservatórios", "value": "reservatorios"},
    {"label": "Nascentes", "value": "nascentes"},
    {"label": "Bacias Hidrográficas", "value": "bacias"},
    {"label": "Estações Hidrológicas", "value": "estacoes_hidro"},
    {"label": "Estações Meteorológicas", "value": "estacoes_meteo"},
]

REGIOES_BRASIL: Final[list[dict[str, str]]] = [
    {"label": "Norte", "value": "norte"},
    {"label": "Nordeste", "value": "nordeste"},
    {"label": "Centro-Oeste", "value": "centro_oeste"},
    {"label": "Sudeste", "value": "sudeste"},
    {"label": "Sul", "value": "sul"},
]
