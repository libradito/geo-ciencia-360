"""
Módulo World Bank — API del Banco Mundial v2
Fuente: Banco Mundial (2023). Indicadores del Desarrollo Mundial. API v2.
Endpoint: http://api.worldbank.org/v2/country/{code}/indicator/{indicator}
Nota: La API del Banco Mundial es ABIERTA (no requiere token).
Referencia ONU: https://unstats.un.org/sdgs/ designa al Banco Mundial como custodio ODS.
"""

import csv
import os

import requests

# ─── Ruta al cache local ──────────────────────────────────────────────
_CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "wb_cache.csv")

# ─── Mapping ODS → código de indicador World Bank ────────────────────
WB_MAP = {
    "ODS1": "SI.POV.DDAY",         # Pobreza < $2.15/día (%)
    "ODS4": "SE.ADT.LITR.ZS",      # Tasa de alfabetización adultos (%)
    "ODS5": "SL.TLF.CACT.FE.ZS",   # Participación fuerza laboral femenina (%)
    "ODS8": "SL.EMP.VULN.ZS",      # Empleo vulnerable (% del total)
}

# ─── Países LATAM para promedio regional ─────────────────────────────
LATAM_CODES = [
    "MEX", "GTM", "HND", "SLV", "NIC", "CRI", "PAN",
    "COL", "VEN", "ECU", "PER", "BOL", "BRA", "CHL",
    "ARG", "URY", "PRY", "DOM", "HTI", "CUB",
]

# ─── URL base ────────────────────────────────────────────────────────
BASE_URL = "https://api.worldbank.org/v2/country/{code}/indicator/{indicator}"


def fetch_wb_indicator(country_code, indicator, date="2022"):
    """
    Consulta un indicador del Banco Mundial para un país o grupo.
    Retorna el valor numérico más reciente o None.
    """
    try:
        url = BASE_URL.format(code=country_code, indicator=indicator)
        params = {
            "format": "json",
            "date": date,
            "per_page": 300,
        }
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        # La API retorna [metadata, [datos]]
        if not isinstance(data, list) or len(data) < 2:
            return None

        records = data[1]
        if not records:
            return None

        # Buscar el primer registro con valor no nulo
        for record in records:
            val = record.get("value")
            if val is not None:
                return float(val)

        return None

    except requests.exceptions.RequestException as e:
        print(f"ERROR World Bank API (request) [{country_code}]: {e}")
        return None
    except (ValueError, KeyError, IndexError, TypeError) as e:
        print(f"ERROR World Bank API (parse) [{country_code}]: {e}")
        return None
    except Exception as e:
        print(f"ERROR World Bank API [{country_code}]: {e}")
        return None


def get_mexico_value(indicator, date="2018:2022"):
    """Obtiene el valor de México para un indicador."""
    return fetch_wb_indicator("MEX", indicator, date)


def get_latam_average(indicator, date="2018:2022"):
    """
    Calcula el promedio LATAM consultando cada país individualmente.
    Usa rango de fechas para maximizar disponibilidad de datos.
    """
    try:
        values = []
        # Consultar región LATAM como grupo
        latam_val = fetch_wb_indicator("LAC", indicator, date)
        if latam_val is not None:
            return latam_val

        # Fallback: promediar países individuales
        for code in LATAM_CODES:
            val = fetch_wb_indicator(code, indicator, date)
            if val is not None:
                values.append(val)

        if values:
            return sum(values) / len(values)
        return None

    except Exception as e:
        print(f"ERROR World Bank get_latam_average: {e}")
        return None


def get_world_average(indicator, date="2018:2022"):
    """Obtiene el promedio mundial usando el código 'WLD'."""
    return fetch_wb_indicator("WLD", indicator, date)


def _load_cache():
    """
    Lee data/wb_cache.csv y retorna un dict {indicator: {"LAC": float, "WLD": float}}.
    Retorna {} si el archivo no existe o no se puede leer.
    """
    try:
        path = os.path.abspath(_CACHE_PATH)
        if not os.path.isfile(path):
            return {}
        cache = {}
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                lac = float(row["LAC"]) if row.get("LAC") not in (None, "", "None") else None
                wld = float(row["WLD"]) if row.get("WLD") not in (None, "", "None") else None
                cache[row["indicator"]] = {"LAC": lac, "WLD": wld}
        return cache
    except Exception as e:
        print(f"AVISO World Bank cache: {e}")
        return {}


def get_worldbank_data(ods):
    """
    Función principal: retorna (latam, world) para un ODS.
    Lee de data/wb_cache.csv si está disponible; si no, consulta la API.
    Si no existe indicador, retorna (None, None).
    """
    indicator = WB_MAP.get(ods)
    if indicator is None:
        return None, None

    try:
        cache = _load_cache()
        entry = cache.get(indicator, {})
        latam = entry.get("LAC")
        world = entry.get("WLD")

        # Respaldo a API solo para los valores que falten en el cache
        if latam is None:
            latam = get_latam_average(indicator)
        if world is None:
            world = get_world_average(indicator)

        return latam, world
    except Exception as e:
        print(f"ERROR World Bank get_worldbank_data: {e}")
        return None, None


def get_wb_url(ods):
    """Retorna la URL de consulta para auditoría."""
    indicator = WB_MAP.get(ods)
    if indicator is None:
        return None
    return f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&date=2022&per_page=300"
