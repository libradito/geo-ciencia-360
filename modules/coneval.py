"""
Módulo CONEVAL — Datos de pobreza municipal 2020
Fuente: Base de Datos de Pobreza Municipal CONEVAL 2020
Datos Abiertos: https://www.coneval.org.mx/Medicion/Paginas/Pobreza-municipio-2010-2020.aspx
BD y Programas: https://www.coneval.org.mx/Medicion/Paginas/Programas_BD_municipal_2010_2020.aspx

Estrategia de carga:
  1. Intenta cargar Excel local (data/coneval_pobreza_municipal.xlsx)
  2. Si no existe, intenta descargar CSV de datos abiertos CONEVAL
  3. Si falla, intenta cargar CSV local (data/coneval_pobreza_municipal.csv)
"""

import os
import pandas as pd

# ─── Rutas ────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
EXCEL_PATH = os.path.join(DATA_DIR, "coneval_pobreza_municipal.xlsx")
CSV_PATH = os.path.join(DATA_DIR, "coneval_pobreza_municipal.csv")

# ─── URL de datos abiertos CONEVAL (CSV) ──────────────────────────────
CONEVAL_CSV_URL = (
    "https://www.coneval.org.mx/Informes/Pobreza/Datos_abiertos/"
    "pobreza_municipal_2010-2020/indicadores de pobreza municipal_2020.csv"
)

# ─── Mapping ODS → columna CONEVAL ───────────────────────────────────
# Nombres pueden variar entre Excel y CSV; probamos variantes
ODS_CONEVAL_MAP = {
    "ODS1": ["pobreza_e", "pobreza_ext"],                      # Pobreza extrema (%) — Chamula: 52.3%
    "ODS4": ["ic_rezedu", "car_ed"],                           # Carencia por rezago educativo (%) — Chamula: 55.3%
    "ODS5": ["ic_segsoc", "ic_asalud"],                        # Carencia seguridad social (proxy género) — Chamula: 91.7%
    "ODS8": ["plp_e", "ing_cor", "plp"],                       # Población bajo línea pobreza extrema por ingreso (%) — Chamula: 76.9%
}

# ─── CVEGEO de Chamula ───────────────────────────────────────────────
CHAMULA_CVEGEO = "07023"


def _find_column(df, candidates):
    """Busca la primera columna que coincida (case-insensitive) de una lista de candidatos."""
    df_cols_lower = {c.lower().strip(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in df_cols_lower:
            return df_cols_lower[candidate.lower()]
    return None


def _find_cvegeo_column(df):
    """Busca la columna CVEGEO en el DataFrame (varios nombres posibles)."""
    candidates = ["clave_municipio", "CVEGEO", "cvegeo", "cve_geo", "CVE_GEO",
                   "foliovuln", "ent_mun", "cve_muni"]
    for candidate in candidates:
        for col in df.columns:
            if candidate.lower() == col.lower().strip():
                return col
    # Fallback: buscar columna que contenga códigos de 5 dígitos
    for col in df.columns:
        sample = df[col].astype(str).str.zfill(5).head(20)
        if sample.str.match(r'^\d{5}$').sum() > 5:
            return col
    return None


def _download_csv():
    """Descarga el CSV de datos abiertos CONEVAL y lo guarda localmente."""
    try:
        import requests
        print("Descargando datos CONEVAL desde datos abiertos...")
        response = requests.get(CONEVAL_CSV_URL, timeout=30)
        response.raise_for_status()

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(CSV_PATH, "wb") as f:
            f.write(response.content)
        print(f"Guardado en: {CSV_PATH}")
        return True
    except Exception as e:
        print(f"ERROR al descargar CSV CONEVAL: {e}")
        return False


def load_coneval_data():
    """
    Carga y limpia los datos de CONEVAL.
    Intenta: Excel local → CSV descargado → CSV local.
    Retorna un DataFrame con CVEGEO como string y columnas numéricas.
    """
    df = None

    # ── Intento 1: Excel local ───────────────────────────────────────
    if os.path.exists(EXCEL_PATH):
        try:
            # Intentar hoja "Concentrado", si no existe usar la primera hoja
            try:
                df = pd.read_excel(EXCEL_PATH, sheet_name="Concentrado")
            except ValueError:
                df = pd.read_excel(EXCEL_PATH, sheet_name=0)
            print(f"Cargado Excel: {EXCEL_PATH} ({len(df)} filas)")
        except Exception as e:
            print(f"Error leyendo Excel: {e}")

    # ── Intento 2: CSV local ─────────────────────────────────────────
    if df is None and os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH, encoding="latin-1")
            print(f"Cargado CSV local: {CSV_PATH} ({len(df)} filas)")
        except Exception as e:
            try:
                df = pd.read_csv(CSV_PATH, encoding="utf-8")
                print(f"Cargado CSV local (utf-8): {CSV_PATH} ({len(df)} filas)")
            except Exception as e2:
                print(f"Error leyendo CSV local: {e2}")

    # ── Intento 3: Descargar CSV ─────────────────────────────────────
    if df is None:
        if _download_csv():
            try:
                df = pd.read_csv(CSV_PATH, encoding="latin-1")
                print(f"Cargado CSV descargado: ({len(df)} filas)")
            except Exception as e:
                try:
                    df = pd.read_csv(CSV_PATH, encoding="utf-8")
                except Exception as e2:
                    print(f"Error leyendo CSV descargado: {e2}")

    if df is None:
        print("ERROR CONEVAL: No se pudo cargar ningún archivo de datos.")
        print(f"  Opciones:")
        print(f"  1. Descarga el Excel de CONEVAL y colócalo en: {EXCEL_PATH}")
        print(f"  2. Descarga el CSV y colócalo en: {CSV_PATH}")
        print(f"  3. Visita: https://www.coneval.org.mx/Medicion/Paginas/Programas_BD_municipal_2010_2020.aspx")
        return None

    # ── Limpiar CVEGEO ───────────────────────────────────────────────
    cvegeo_col = _find_cvegeo_column(df)
    if cvegeo_col:
        if cvegeo_col != "CVEGEO":
            df.rename(columns={cvegeo_col: "CVEGEO"}, inplace=True)
        df["CVEGEO"] = df["CVEGEO"].astype(str).str.zfill(5)
    else:
        print("ADVERTENCIA CONEVAL: No se encontró columna CVEGEO")

    # ── Convertir columnas numéricas ─────────────────────────────────
    for candidates in ODS_CONEVAL_MAP.values():
        col = _find_column(df, candidates)
        if col:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def map_ods_to_column(ods):
    """Retorna el nombre de columna CONEVAL para un ODS dado."""
    candidates = ODS_CONEVAL_MAP.get(ods, [])
    if not candidates:
        return None
    # Si ya tenemos un DataFrame cargado, buscamos la columna real
    # Por ahora retornamos el primer candidato
    return candidates[0] if candidates else None


def get_chamula_value(df, col):
    """Extrae el valor de Chamula (CVEGEO 07023) para una columna dada."""
    if df is None or col is None:
        return None
    try:
        # Buscar la columna real (puede tener nombre diferente)
        real_col = _find_column(df, [col])
        if real_col is None:
            print(f"ADVERTENCIA: Columna '{col}' no encontrada. Columnas disponibles: {list(df.columns[:20])}")
            return None

        if "CVEGEO" not in df.columns:
            print("ADVERTENCIA: Columna CVEGEO no encontrada en DataFrame")
            return None

        row = df[df["CVEGEO"] == CHAMULA_CVEGEO]
        if row.empty:
            # Intentar sin ceros a la izquierda
            row = df[df["CVEGEO"] == "7023"]
        if row.empty:
            print(f"ADVERTENCIA: Chamula (CVEGEO {CHAMULA_CVEGEO}) no encontrado")
            return None

        val = row[real_col].values[0]
        return float(val) if pd.notna(val) else None
    except Exception as e:
        print(f"ERROR CONEVAL get_chamula_value: {e}")
        return None


def get_national_avg(df, col):
    """Calcula el promedio nacional para una columna dada."""
    if df is None or col is None:
        return None
    try:
        real_col = _find_column(df, [col])
        if real_col is None:
            return None

        vals = pd.to_numeric(df[real_col], errors="coerce")
        avg = vals.mean()
        return float(avg) if pd.notna(avg) else None
    except Exception as e:
        print(f"ERROR CONEVAL get_national_avg: {e}")
        return None


def get_coneval_indicator(ods):
    """
    Función principal: retorna (chamula_value, national_avg) para un ODS.
    Si no existe columna para el ODS, retorna (None, None).
    """
    candidates = ODS_CONEVAL_MAP.get(ods, [])
    if not candidates:
        return None, None

    df = load_coneval_data()
    if df is None:
        return None, None

    # Intentar cada nombre candidato hasta encontrar uno que funcione
    for col_name in candidates:
        real_col = _find_column(df, [col_name])
        if real_col:
            chamula = get_chamula_value(df, col_name)
            nacional = get_national_avg(df, col_name)
            if chamula is not None or nacional is not None:
                return chamula, nacional

    return None, None
