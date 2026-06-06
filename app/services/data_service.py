"""Serviço de dados territoriais — cobertura nacional."""

from __future__ import annotations

import json
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from app.core.brasil import BACIAS_POR_REGIAO, CIDADES_POR_UF, ESTADOS_BRASIL, get_estado
from app.core.helpers import filter_dataframe

DATA_DIR = Path(__file__).parent.parent.parent / "data"
GEOJSON_DIR = DATA_DIR / "geojson"
RNG = np.random.default_rng(42)


class DataService:
    """Gera e serve dados simulados para todo o Brasil."""

    _cache: dict[str, tuple[float, Any]] = {}
    _ttl = 300

    def _cache_get(self, key: str) -> Any | None:
        entry = self._cache.get(key)
        if entry and (time.time() - entry[0]) < self._ttl:
            return entry[1]
        return None

    def _cache_set(self, key: str, value: Any) -> None:
        self._cache[key] = (time.time(), value)

    def _coord_for_estado(self, uf: str) -> tuple[float, float]:
        estado = get_estado(uf)
        if not estado:
            return -15.0, -47.0
        lat = float(RNG.uniform(estado["lat_min"], estado["lat_max"]))
        lon = float(RNG.uniform(estado["lon_min"], estado["lon_max"]))
        return lat, lon

    @staticmethod
    def _random_status() -> str:
        return str(RNG.choice(
            ["normal", "atencao", "critico", "sem_dados"],
            p=[0.45, 0.30, 0.15, 0.10],
        ))

    def get_estados(self) -> list[dict[str, str]]:
        """Lista todos os estados + opção Brasil."""
        estados = [{"label": "Brasil (Nacional)", "value": "BR"}]
        for e in ESTADOS_BRASIL:
            estados.append({"label": e["nome"], "value": e["uf"]})
        return estados

    def get_municipios(self, **filters: Any) -> pd.DataFrame:
        """Municípios simulados para todas as UFs."""
        cache_key = "municipios_br"
        cached = self._cache_get(cache_key)
        if cached is None:
            records = []
            idx = 0
            for estado in ESTADOS_BRASIL:
                uf = estado["uf"]
                cidades = [estado["capital"], *(CIDADES_POR_UF.get(uf, [])[:4])]
                bacias = BACIAS_POR_REGIAO[estado["regiao"]]
                for cidade in cidades:
                    lat, lon = self._coord_for_estado(uf)
                    bacia = bacias[idx % len(bacias)]
                    pop = int(RNG.integers(50_000, 2_000_000))
                    records.append({
                        "id": f"mun_{uf}_{idx:04d}",
                        "nome": cidade,
                        "estado": uf,
                        "estado_nome": estado["nome"],
                        "regiao": estado["regiao"],
                        "bacia": bacia,
                        "populacao": pop,
                        "indice_hidrico": round(float(RNG.uniform(35, 85)), 1),
                        "status": self._random_status(),
                        "lat": lat,
                        "lon": lon,
                    })
                    idx += 1
            cached = pd.DataFrame(records)
            self._cache_set(cache_key, cached)
        return filter_dataframe(cached, **filters)

    def get_recursos(self, **filters: Any) -> pd.DataFrame:
        """Recursos hídricos simulados."""
        cache_key = "recursos_br"
        cached = self._cache_get(cache_key)
        if cached is None:
            municipios = self.get_municipios()
            records = []
            rid = 1
            for tipo, per_uf in [("reservatorio", 3), ("represa", 2), ("nascente", 4), ("rio", 2)]:
                for estado in ESTADOS_BRASIL:
                    mun_subset = municipios[municipios["estado"] == estado["uf"]]
                    if mun_subset.empty:
                        continue
                    for _ in range(per_uf):
                        mun = mun_subset.sample(1, random_state=rid).iloc[0]
                        lat, lon = self._coord_for_estado(estado["uf"])
                        cap = float(RNG.uniform(10, 800)) if tipo in ("reservatorio", "represa") else None
                        nivel = float(RNG.uniform(15, 95)) if cap else None
                        vol = (cap * nivel / 100) if cap and nivel else None
                        records.append({
                            "id": f"rec_{rid:05d}",
                            "nome": f"{tipo.title()} {mun['nome']}",
                            "tipo": tipo,
                            "municipio_id": mun["id"],
                            "municipio_nome": mun["nome"],
                            "estado": estado["uf"],
                            "bacia": mun["bacia"],
                            "regiao": mun["regiao"],
                            "capacidade_hm3": cap,
                            "volume_atual_hm3": vol,
                            "nivel_percentual": nivel,
                            "vazao_m3s": float(RNG.uniform(5, 500)),
                            "chuva_mm": float(RNG.uniform(0, 150)),
                            "status": self._random_status(),
                            "populacao_impactada": int(mun["populacao"] * float(RNG.uniform(0.01, 0.12))),
                            "lat": lat,
                            "lon": lon,
                        })
                        rid += 1
            cached = pd.DataFrame(records)
            self._cache_set(cache_key, cached)
        return filter_dataframe(cached, **filters)

    def get_estacoes(self, **filters: Any) -> pd.DataFrame:
        """Estações hidrológicas e pluviométricas."""
        cache_key = "estacoes_br"
        cached = self._cache_get(cache_key)
        if cached is None:
            municipios = self.get_municipios()
            records = []
            eid = 1
            for estado in ESTADOS_BRASIL:
                mun_subset = municipios[municipios["estado"] == estado["uf"]]
                for i in range(3):
                    if mun_subset.empty:
                        break
                    mun = mun_subset.iloc[i % len(mun_subset)]
                    lat, lon = self._coord_for_estado(estado["uf"])
                    tipo = "estacao_hidro" if i % 2 == 0 else "estacao_pluvio"
                    records.append({
                        "id": f"est_{eid:05d}",
                        "nome": f"Est. {'Hidro' if tipo == 'estacao_hidro' else 'Pluvio'} {mun['nome']}",
                        "tipo": tipo,
                        "municipio_id": mun["id"],
                        "municipio_nome": mun["nome"],
                        "estado": estado["uf"],
                        "bacia": mun["bacia"],
                        "nivel_m": float(RNG.uniform(1, 20)) if tipo == "estacao_hidro" else None,
                        "vazao_m3s": float(RNG.uniform(10, 600)) if tipo == "estacao_hidro" else None,
                        "chuva_mm": float(RNG.uniform(0, 180)),
                        "status": self._random_status(),
                        "lat": lat,
                        "lon": lon,
                    })
                    eid += 1
            cached = pd.DataFrame(records)
            self._cache_set(cache_key, cached)
        return filter_dataframe(cached, **filters)

    def get_kpis(self, **filters: Any) -> dict[str, Any]:
        """KPIs agregados."""
        recursos = self.get_recursos(**filters)
        municipios = self.get_municipios(**filters)
        reserv = recursos[recursos["tipo"].isin(["reservatorio", "represa"])]
        alerta = municipios[municipios["status"].isin(["atencao", "critico"])]
        vol = reserv["volume_atual_hm3"].sum()
        return {
            "reservatorios_monitorados": len(reserv),
            "municipios_alerta": len(alerta),
            "volume_total_hm3": round(float(vol), 1) if not pd.isna(vol) else 0,
            "populacao_impactada": int(recursos["populacao_impactada"].sum()),
            "indice_hidrico_medio": round(float(municipios["indice_hidrico"].mean()), 1),
            "ocorrencias_criticas": int((recursos["status"] == "critico").sum()),
        }

    def get_serie_temporal(self, indicador: str = "nivel_reservatorio", periodo: str = "30d") -> pd.DataFrame:
        """Série temporal simulada."""
        days_map = {"7d": 7, "30d": 30, "90d": 90, "1y": 365, "all": 730}
        days = days_map.get(periodo, 30)
        dates = pd.date_range(end=pd.Timestamp.now(), periods=days, freq="D")
        if indicador == "nivel_reservatorio":
            values = np.clip(55 + RNG.normal(0, 3, days) + np.linspace(0, -8, days), 10, 95)
        elif indicador == "chuva":
            values = np.clip(RNG.exponential(8, days), 0, 80)
        else:
            values = 120 + RNG.normal(0, 15, days)
        return pd.DataFrame({"data": dates.astype(str), "valor": values.round(2), "indicador": indicador})

    def get_ranking_municipios(self, **filters: Any) -> pd.DataFrame:
        df = self.get_municipios(**filters).copy()
        order = {"critico": 0, "atencao": 1, "sem_dados": 2, "normal": 3}
        df["ordem"] = df["status"].map(order)
        return df.sort_values(["ordem", "indice_hidrico"]).head(10)

    def get_volume_por_bacia(self, **filters: Any) -> pd.DataFrame:
        rec = self.get_recursos(**filters)
        res = rec[rec["tipo"].isin(["reservatorio", "represa"])]
        return (
            res.groupby("bacia", as_index=False)["volume_atual_hm3"]
            .sum()
            .rename(columns={"volume_atual_hm3": "volume_hm3"})
            .sort_values("volume_hm3", ascending=False)
        )

    def get_vulnerabilidade_regiao(self, **filters: Any) -> pd.DataFrame:
        mun = self.get_municipios(**filters)
        return (
            mun.groupby("regiao", as_index=False)
            .agg(
                indice_hidrico=("indice_hidrico", "mean"),
                populacao=("populacao", "sum"),
                municipios_criticos=("status", lambda x: (x == "critico").sum()),
            )
            .sort_values("indice_hidrico")
        )

    def get_tabela(self, **filters: Any) -> pd.DataFrame:
        rec = self.get_recursos(**filters)
        return rec[[
            "id", "nome", "tipo", "municipio_nome", "estado", "bacia", "regiao",
            "nivel_percentual", "volume_atual_hm3", "vazao_m3s", "chuva_mm",
            "status", "populacao_impactada",
        ]].rename(columns={
            "municipio_nome": "municipio",
            "nivel_percentual": "nivel_pct",
            "volume_atual_hm3": "volume_hm3",
            "populacao_impactada": "pop_impactada",
        })

    def get_map_points(self, layers: list[str] | None = None, **filters: Any) -> list[dict[str, Any]]:
        """Pontos para o mapa."""
        layers = layers or ["municipios", "reservatorios"]
        points: list[dict[str, Any]] = []

        if "municipios" in layers:
            for _, r in self.get_municipios(**filters).iterrows():
                points.append({
                    "id": r["id"], "nome": r["nome"], "lat": r["lat"], "lon": r["lon"],
                    "tipo": "municipio", "status": r["status"], "valor": r["indice_hidrico"],
                    "camada": "municipios", "estado": r["estado"],
                })

        if "reservatorios" in layers or "nascentes" in layers:
            tipos = []
            if "reservatorios" in layers:
                tipos.extend(["reservatorio", "represa"])
            if "nascentes" in layers:
                tipos.append("nascente")
            for _, r in self.get_recursos(**filters).iterrows():
                if r["tipo"] in tipos:
                    points.append({
                        "id": r["id"], "nome": r["nome"], "lat": r["lat"], "lon": r["lon"],
                        "tipo": r["tipo"], "status": r["status"],
                        "valor": r.get("nivel_percentual"), "camada": "reservatorios",
                        "estado": r["estado"],
                    })

        if "estacoes_hidro" in layers or "estacoes_meteo" in layers:
            tipos_e = []
            if "estacoes_hidro" in layers:
                tipos_e.append("estacao_hidro")
            if "estacoes_meteo" in layers:
                tipos_e.append("estacao_pluvio")
            for _, r in self.get_estacoes(**filters).iterrows():
                if r["tipo"] in tipos_e:
                    points.append({
                        "id": r["id"], "nome": r["nome"], "lat": r["lat"], "lon": r["lon"],
                        "tipo": r["tipo"], "status": r["status"],
                        "valor": r.get("nivel_m") or r.get("chuva_mm"),
                        "camada": "estacoes", "estado": r["estado"],
                    })

        return points

    def get_map_center(self, estado: str = "BR") -> dict[str, Any]:
        """Centro e zoom do mapa conforme escopo."""
        if estado == "BR":
            return {"lat": -14.235, "lon": -51.925, "zoom": 4}
        info = get_estado(estado)
        if info:
            lat = (info["lat_min"] + info["lat_max"]) / 2
            lon = (info["lon_min"] + info["lon_max"]) / 2
            return {"lat": lat, "lon": lon, "zoom": 7}
        return {"lat": -14.235, "lon": -51.925, "zoom": 4}


@lru_cache(maxsize=1)
def get_data_service() -> DataService:
    return DataService()
