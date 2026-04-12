"""
Módulo CORE — Integración de todas las fuentes de datos
CONTRATO GLOBAL (NO ROMPER)

def get_ods_data(ods) -> dict:
    return {
        "chamula": float,       # Valor Chamula (CONEVAL)
        "nacional": float,      # Promedio nacional (CONEVAL)
        "latam": float,         # Promedio LATAM (Banco Mundial)
        "world": float,         # Promedio mundial (Banco Mundial)
        "brecha": float,        # chamula / nacional
        "fuentes": {            # Panel de auditoría anti-alucinación
            "chamula": {...},
            "nacional": {...},
            "latam": {...},
            "world": {...},
        }
    }

Todo el sistema depende de esto.
"""

from modules.coneval import (
    load_coneval_data,
    get_chamula_value,
    get_national_avg,
    ODS_CONEVAL_MAP,
    _find_column,
)
from modules.inegi import get_inegi_data, get_inegi_url, ODS_INEGI_MAP
from modules.worldbank import (
    get_worldbank_data,
    get_wb_url,
    WB_MAP,
)

# ─── Nombres legibles de los ODS ─────────────────────────────────────
ODS_NOMBRES = {
    "ODS1": "ODS 1 — Fin de la Pobreza",
    "ODS4": "ODS 4 — Educación de Calidad",
    "ODS5": "ODS 5 — Igualdad de Género",
    "ODS8": "ODS 8 — Trabajo Decente y Crecimiento Económico",
}

ODS_DESCRIPCION = {
    "ODS1": "Porcentaje de población en pobreza extrema",
    "ODS4": "Carencia por rezago educativo / Tasa de alfabetización",
    "ODS5": "Participación de la mujer en la fuerza laboral",
    "ODS8": "Ingreso corriente per cápita / Empleo vulnerable",
}


def _resolve_coneval_column(df, ods):
    """Resuelve el nombre real de la columna CONEVAL para un ODS."""
    candidates = ODS_CONEVAL_MAP.get(ods, [])
    for col_name in candidates:
        real_col = _find_column(df, [col_name])
        if real_col:
            return real_col
    return None


def build_fuentes(ods, col):
    """
    Construye el diccionario de auditoría (anti-alucinación).
    Cada número del dashboard es rastreable hasta su fuente original.
    """
    indicator_wb = WB_MAP.get(ods)
    indicator_inegi = ODS_INEGI_MAP.get(ods)
    col_display = col if col else "N/A (sin indicador CONEVAL para este ODS)"

    fuentes = {
        "chamula": {
            "fuente": "CONEVAL",
            "sistema": "Anexo Estadístico de Pobreza Municipal 2010-2020",
            "url": "https://www.coneval.org.mx/Medicion/Paginas/Pobreza-municipio-2010-2020.aspx",
            "archivo": "Indicadores de pobreza municipal 2020 (Datos Abiertos CONEVAL)",
            "consulta": f"CVEGEO=07023, columna={col_display}",
            "periodicidad": "Bienal. Última actualización: 2020",
        },
        "nacional": {
            "fuente": "CONEVAL",
            "sistema": "Anexo Estadístico de Pobreza Municipal 2010-2020",
            "url": "https://www.coneval.org.mx/Medicion/Paginas/Pobreza-municipio-2010-2020.aspx",
            "consulta": f"Promedio nacional de 2,469 municipios, columna={col_display}",
            "periodicidad": "Bienal. Última actualización: 2020",
        },
        "latam": {
            "fuente": "Banco Mundial",
            "sistema": "World Development Indicators API v2",
            "url": f"https://api.worldbank.org/v2/country/LAC/indicator/{indicator_wb}?format=json&date=2022",
            "consulta": f"indicator={indicator_wb}, region=LAC",
            "periodicidad": "Anual",
            "custodio_onu": "https://unstats.un.org/sdgs/",
        },
        "world": {
            "fuente": "Banco Mundial",
            "sistema": "World Development Indicators API v2",
            "url": f"https://api.worldbank.org/v2/country/WLD/indicator/{indicator_wb}?format=json&date=2022",
            "consulta": f"indicator={indicator_wb}, region=WLD",
            "periodicidad": "Anual",
            "custodio_onu": "https://unstats.un.org/sdgs/",
        },
    }

    # Agregar fuente INEGI si aplica
    if indicator_inegi:
        fuentes["inegi_chiapas"] = {
            "fuente": "INEGI",
            "sistema": "API de Indicadores, Banco de Información Económica",
            "url": (
                f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/"
                f"jsonxml/INDICADOR/{indicator_inegi}/es/0700/false/BISE/2.0/TOKEN/json"
            ),
            "consulta": f"indicator_id={indicator_inegi}, entidad=07 (Chiapas)",
            "periodicidad": "Variable según indicador",
        }

    return fuentes


def get_ods_data(ods):
    """
    FUNCIÓN PRINCIPAL — Todo el sistema depende de esto.

    Retorna un diccionario con todos los datos necesarios para UI + auditoría.
    Si falla alguna fuente, el valor correspondiente es None.
    Nunca lanza excepciones — siempre retorna dict o None.
    """
    try:
        # ── CONEVAL (Chamula + Nacional) ─────────────────────────────
        df = load_coneval_data()
        col = None
        chamula = None
        nacional = None

        if df is not None:
            col = _resolve_coneval_column(df, ods)
            if col:
                chamula = get_chamula_value(df, col)
                nacional = get_national_avg(df, col)

        # ── WORLD BANK (LATAM + World) ───────────────────────────────
        latam, world = get_worldbank_data(ods)

        # ── BRECHA ───────────────────────────────────────────────────
        brecha = None
        if chamula is not None and nacional is not None and nacional != 0:
            brecha = chamula / nacional

        # ── FUENTES (Auditoría) ──────────────────────────────────────
        fuentes = build_fuentes(ods, col)

        return {
            "ods": ods,
            "nombre": ODS_NOMBRES.get(ods, ods),
            "descripcion": ODS_DESCRIPCION.get(ods, ""),
            "chamula": chamula,
            "nacional": nacional,
            "latam": latam,
            "world": world,
            "brecha": brecha,
            "fuentes": fuentes,
        }

    except Exception as e:
        print(f"ERROR CORE: {e}")
        return None
