"""Metadados territoriais do Brasil — 27 UFs."""

from __future__ import annotations

from typing import TypedDict


class EstadoInfo(TypedDict):
    """Informações de um estado brasileiro."""

    uf: str
    nome: str
    regiao: str
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    capital: str


ESTADOS_BRASIL: list[EstadoInfo] = [
    {"uf": "AC", "nome": "Acre", "regiao": "norte", "lat_min": -11.0, "lat_max": -7.0, "lon_min": -74.0, "lon_max": -66.5, "capital": "Rio Branco"},
    {"uf": "AL", "nome": "Alagoas", "regiao": "nordeste", "lat_min": -10.5, "lat_max": -8.8, "lon_min": -38.5, "lon_max": -35.0, "capital": "Maceió"},
    {"uf": "AP", "nome": "Amapá", "regiao": "norte", "lat_min": 2.0, "lat_max": 4.5, "lon_min": -54.0, "lon_max": -49.5, "capital": "Macapá"},
    {"uf": "AM", "nome": "Amazonas", "regiao": "norte", "lat_min": -9.0, "lat_max": 2.0, "lon_min": -74.0, "lon_max": -56.0, "capital": "Manaus"},
    {"uf": "BA", "nome": "Bahia", "regiao": "nordeste", "lat_min": -18.5, "lat_max": -8.5, "lon_min": -46.5, "lon_max": -37.5, "capital": "Salvador"},
    {"uf": "CE", "nome": "Ceará", "regiao": "nordeste", "lat_min": -7.5, "lat_max": -2.8, "lon_min": -41.5, "lon_max": -37.0, "capital": "Fortaleza"},
    {"uf": "DF", "nome": "Distrito Federal", "regiao": "centro_oeste", "lat_min": -16.0, "lat_max": -15.5, "lon_min": -48.2, "lon_max": -47.3, "capital": "Brasília"},
    {"uf": "ES", "nome": "Espírito Santo", "regiao": "sudeste", "lat_min": -21.5, "lat_max": -17.9, "lon_min": -41.5, "lon_max": -39.5, "capital": "Vitória"},
    {"uf": "GO", "nome": "Goiás", "regiao": "centro_oeste", "lat_min": -19.5, "lat_max": -12.5, "lon_min": -53.5, "lon_max": -45.5, "capital": "Goiânia"},
    {"uf": "MA", "nome": "Maranhão", "regiao": "nordeste", "lat_min": -10.5, "lat_max": -1.0, "lon_min": -48.5, "lon_max": -41.5, "capital": "São Luís"},
    {"uf": "MT", "nome": "Mato Grosso", "regiao": "centro_oeste", "lat_min": -18.0, "lat_max": -7.5, "lon_min": -61.5, "lon_max": -50.0, "capital": "Cuiabá"},
    {"uf": "MS", "nome": "Mato Grosso do Sul", "regiao": "centro_oeste", "lat_min": -24.0, "lat_max": -17.5, "lon_min": -58.5, "lon_max": -50.0, "capital": "Campo Grande"},
    {"uf": "MG", "nome": "Minas Gerais", "regiao": "sudeste", "lat_min": -23.0, "lat_max": -14.0, "lon_min": -51.5, "lon_max": -39.5, "capital": "Belo Horizonte"},
    {"uf": "PA", "nome": "Pará", "regiao": "norte", "lat_min": -10.0, "lat_max": 2.5, "lon_min": -58.5, "lon_max": -46.0, "capital": "Belém"},
    {"uf": "PB", "nome": "Paraíba", "regiao": "nordeste", "lat_min": -8.5, "lat_max": -6.0, "lon_min": -38.8, "lon_max": -34.5, "capital": "João Pessoa"},
    {"uf": "PR", "nome": "Paraná", "regiao": "sul", "lat_min": -26.5, "lat_max": -22.5, "lon_min": -54.5, "lon_max": -48.0, "capital": "Curitiba"},
    {"uf": "PE", "nome": "Pernambuco", "regiao": "nordeste", "lat_min": -9.5, "lat_max": -7.0, "lon_min": -41.5, "lon_max": -34.5, "capital": "Recife"},
    {"uf": "PI", "nome": "Piauí", "regiao": "nordeste", "lat_min": -11.0, "lat_max": -4.5, "lon_min": -45.5, "lon_max": -40.5, "capital": "Teresina"},
    {"uf": "RJ", "nome": "Rio de Janeiro", "regiao": "sudeste", "lat_min": -23.5, "lat_max": -20.5, "lon_min": -45.0, "lon_max": -40.5, "capital": "Rio de Janeiro"},
    {"uf": "RN", "nome": "Rio Grande do Norte", "regiao": "nordeste", "lat_min": -6.5, "lat_max": -4.8, "lon_min": -38.5, "lon_max": -34.8, "capital": "Natal"},
    {"uf": "RS", "nome": "Rio Grande do Sul", "regiao": "sul", "lat_min": -34.0, "lat_max": -27.0, "lon_min": -57.5, "lon_max": -49.5, "capital": "Porto Alegre"},
    {"uf": "RO", "nome": "Rondônia", "regiao": "norte", "lat_min": -13.5, "lat_max": -7.5, "lon_min": -66.5, "lon_max": -59.5, "capital": "Porto Velho"},
    {"uf": "RR", "nome": "Roraima", "regiao": "norte", "lat_min": 0.5, "lat_max": 5.5, "lon_min": -64.5, "lon_max": -59.0, "capital": "Boa Vista"},
    {"uf": "SC", "nome": "Santa Catarina", "regiao": "sul", "lat_min": -29.5, "lat_max": -25.5, "lon_min": -53.5, "lon_max": -48.0, "capital": "Florianópolis"},
    {"uf": "SP", "nome": "São Paulo", "regiao": "sudeste", "lat_min": -24.5, "lat_max": -19.5, "lon_min": -53.5, "lon_max": -44.0, "capital": "São Paulo"},
    {"uf": "SE", "nome": "Sergipe", "regiao": "nordeste", "lat_min": -11.5, "lat_max": -9.5, "lon_min": -38.5, "lon_max": -36.5, "capital": "Aracaju"},
    {"uf": "TO", "nome": "Tocantins", "regiao": "norte", "lat_min": -13.5, "lat_max": -5.5, "lon_min": -50.5, "lon_max": -45.5, "capital": "Palmas"},
]

# Cidades adicionais por UF para mock nacional
CIDADES_POR_UF: dict[str, list[str]] = {
    "SP": ["Campinas", "Santos", "Ribeirão Preto", "Sorocaba", "Guarulhos"],
    "RJ": ["Niterói", "Campos dos Goytacazes", "Petrópolis", "Volta Redonda"],
    "MG": ["Uberlândia", "Contagem", "Juiz de Fora", "Betim", "Montes Claros"],
    "BA": ["Feira de Santana", "Vitória da Conquista", "Ilhéus", "Juazeiro"],
    "RS": ["Caxias do Sul", "Pelotas", "Canoas", "Santa Maria"],
    "PR": ["Londrina", "Maringá", "Ponta Grossa", "Cascavel"],
    "PE": ["Jaboatão dos Guararapes", "Caruaru", "Petrolina"],
    "CE": ["Caucaia", "Juazeiro do Norte", "Sobral"],
    "PA": ["Ananindeua", "Santarém", "Marabá"],
    "GO": ["Aparecida de Goiânia", "Anápolis", "Rio Verde"],
    "MA": ["Imperatriz", "São José de Ribamar", "Timon"],
    "AM": ["Parintins", "Itacoatiara", "Manacapuru"],
    "SC": ["Joinville", "Blumenau", "Chapecó"],
    "PB": ["Campina Grande", "Santa Rita", "Patos"],
    "ES": ["Vila Velha", "Serra", "Cariacica"],
    "MT": ["Várzea Grande", "Rondonópolis", "Sinop"],
    "MS": ["Dourados", "Três Lagoas", "Corumbá"],
    "DF": ["Taguatinga", "Ceilândia", "Samambaia"],
    "AL": ["Arapiraca", "Rio Largo", "Palmeira dos Índios"],
    "RN": ["Mossoró", "Parnamirim", "Caicó"],
    "PI": ["Parnaíba", "Picos", "Floriano"],
    "SE": ["Nossa Senhora do Socorro", "Lagarto", "Itabaiana"],
    "RO": ["Ji-Paraná", "Ariquemes", "Vilhena"],
    "AC": ["Cruzeiro do Sul", "Sena Madureira", "Tarauacá"],
    "AP": ["Santana", "Laranjal do Jari", "Oiapoque"],
    "RR": ["Rorainópolis", "Caracaraí", "Alto Alegre"],
    "TO": ["Araguaína", "Gurupi", "Porto Nacional"],
}

BACIAS_POR_REGIAO: dict[str, list[str]] = {
    "norte": ["amazonas", "tocantins_araguaia", "xingu"],
    "nordeste": ["saofrancisco", "paranaiba", "paraeperacu"],
    "centro_oeste": ["parana", "paraguai", "tocantins"],
    "sudeste": ["alto_tiete", "paraiba_sul", "grande", "doce"],
    "sul": ["uruguai", "iguacu", "paranapanema"],
}


def get_estado(uf: str) -> EstadoInfo | None:
    """Retorna metadados de um estado."""
    for estado in ESTADOS_BRASIL:
        if estado["uf"] == uf.upper():
            return estado
    return None
