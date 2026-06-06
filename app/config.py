"""Configuração do backend ARANDU."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class DatabaseSettings:
    """Parâmetros PostgreSQL/PostGIS."""

    host: str = "localhost"
    port: int = 5432
    name: str = "arandu"
    user: str = "arandu"
    password: str = "arandu"

    @property
    def url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass(frozen=True)
class Settings:
    """Parâmetros da API."""

    app_name: str = "ARANDU API"
    version: str = "2.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = field(default_factory=lambda: [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ])
    use_mock_data: bool = True
    database: DatabaseSettings = field(default_factory=DatabaseSettings)

    @classmethod
    def from_env(cls) -> Settings:
        """Carrega configuração de variáveis de ambiente."""
        origins = os.getenv(
            "ARANDU_CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        )
        return cls(
            debug=os.getenv("ARANDU_DEBUG", "true").lower() == "true",
            host=os.getenv("ARANDU_API_HOST", "0.0.0.0"),
            port=int(os.getenv("ARANDU_API_PORT", "8000")),
            cors_origins=[o.strip() for o in origins.split(",") if o.strip()],
            use_mock_data=os.getenv("ARANDU_USE_MOCK", "true").lower() == "true",
            database=DatabaseSettings(
                host=os.getenv("ARANDU_DB_HOST", "localhost"),
                port=int(os.getenv("ARANDU_DB_PORT", "5432")),
                name=os.getenv("ARANDU_DB_NAME", "arandu"),
                user=os.getenv("ARANDU_DB_USER", "arandu"),
                password=os.getenv("ARANDU_DB_PASSWORD", "arandu"),
            ),
        )


settings = Settings.from_env()
