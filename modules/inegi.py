"""
Módulo INEGI — API de Indicadores del INEGI
Fuente: Instituto Nacional de Estadística y Geografía
Sistema: Banco de Información Económica (BIE) / Indicadores
Token: a388a068-7c9a-7aef-5768-9021370b96e9
Endpoint: https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/
"""

import requests

# ─── Token INEGI ─────────────────────────────────────────────────────
INEGI_TOKEN = "a388a068-7c9a-7aef-5768-9021370b96e9"

# ─── Mapping ODS → ID de indicador INEGI ─────────────────────────────
# Entidad: 07 = Chiapas
ODS_INEGI_MAP = {
    "ODS1": "6200027861",    # Indicador de pobreza
    "ODS4": "1002000034",    # Indicador educativo
    "ODS5": "6200030882",    # Indicador de género
    "ODS8": "6200030885",    # Indicador económico / empleo
}

# ─── Entidad federativa ──────────────────────────────────────────────
ENTIDAD_CHIAPAS = "07"

# ─── URL base ────────────────────────────────────────────────────────
BASE_URL = (
    "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/"
    "INDICADOR/{indicator_id}/es/{cve_ent}/false/BISE/2.0/{token}/json"
)


def build_inegi_url(indicator_id, cve_ent="0700"):
    """Construye la URL para consultar un indicador INEGI."""
    return BASE_URL.format(
        indicator_id=indicator_id,
        cve_ent=cve_ent,
        token=INEGI_TOKEN,
    )


def fetch_inegi_value(indicator_id, cve_ent="0700"):
    """
    Consulta un indicador INEGI y retorna el valor más reciente.
    cve_ent: '0700' para Chiapas, '00' para nacional.
    """
    try:
        url = build_inegi_url(indicator_id, cve_ent)
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Navegar la estructura de respuesta INEGI
        series = data.get("Series", [])
        if not series:
            return None

        observations = series[0].get("OBSERVATIONS", [])
        if not observations:
            return None

        # Tomar el valor más reciente (último en la lista)
        latest = observations[-1]
        value = latest.get("OBS_VALUE")

        if value is not None:
            return float(value)
        return None

    except requests.exceptions.RequestException as e:
        print(f"ERROR INEGI API (request): {e}")
        return None
    except (ValueError, KeyError, IndexError, TypeError) as e:
        print(f"ERROR INEGI API (parse): {e}")
        return None
    except Exception as e:
        print(f"ERROR INEGI API: {e}")
        return None


def get_inegi_data(ods):
    """
    Función principal: retorna el valor estatal de Chiapas para un ODS.
    Si no existe indicador para el ODS, retorna None.
    """
    indicator_id = ODS_INEGI_MAP.get(ods)
    if indicator_id is None:
        return None

    try:
        # Valor para Chiapas (entidad 07)
        value = fetch_inegi_value(indicator_id, cve_ent="0700")
        return value
    except Exception as e:
        print(f"ERROR INEGI get_inegi_data: {e}")
        return None


def get_inegi_url(ods):
    """Retorna la URL de consulta para auditoría."""
    indicator_id = ODS_INEGI_MAP.get(ods)
    if indicator_id is None:
        return None
    return build_inegi_url(indicator_id, cve_ent="0700")
