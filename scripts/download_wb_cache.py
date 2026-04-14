"""
Script: download_wb_cache.py
Descarga los 8 valores del Banco Mundial que usa el dashboard y los guarda
en data/wb_cache.csv. Ejecutar una vez al año cuando se quieran datos frescos.

Uso:
    python scripts/download_wb_cache.py
"""

import csv
import os
import sys
from datetime import date

import requests

# Asegurar que podemos importar desde modules/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.worldbank import WB_MAP

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "wb_cache.csv")
YEARS = [2022, 2021, 2020, 2019, 2018]   # intenta desde el más reciente


def fetch_value(country_code, indicator, timeout=20):
    """
    Intenta obtener un valor del Banco Mundial probando años de más reciente a más antiguo.
    Construye la URL manualmente para evitar que requests codifique el año como %3A.
    Si country_code='LAC' y no hay datos, reintenta con 'LCN' (código alternativo LATAM).
    """
    codes_to_try = [country_code]
    if country_code == "LAC":
        codes_to_try.append("LCN")   # código alternativo Banco Mundial para LATAM

    for code in codes_to_try:
        base = f"https://api.worldbank.org/v2/country/{code}/indicator/{indicator}"
        for year in YEARS:
            url = f"{base}?format=json&date={year}&per_page=10"
            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                data = response.json()
                if not isinstance(data, list) or len(data) < 2:
                    continue
                records = data[1]
                if not records:
                    continue
                for record in records:
                    val = record.get("value")
                    if val is not None:
                        return float(val), year
            except requests.exceptions.Timeout:
                print(f"      timeout ({code}/{year}), reintentando...")
                continue
            except Exception as e:
                print(f"      error ({code}/{year}): {e}")
                continue
    return None, None


def main():
    today = date.today().isoformat()
    rows = []

    print("Descargando indicadores del Banco Mundial...")
    print(f"Intentando años: {YEARS}\n")

    for ods, indicator in WB_MAP.items():
        print(f"  [{ods}] {indicator}")

        lac, lac_year = fetch_value("LAC", indicator)
        wld, wld_year = fetch_value("WLD", indicator)

        lac = round(lac, 2) if lac is not None else None
        wld = round(wld, 2) if wld is not None else None

        print(f"         LAC={lac} ({lac_year})  WLD={wld} ({wld_year})")

        rows.append({
            "indicator": indicator,
            "LAC": lac,
            "WLD": wld,
            "downloaded": today,
            "year_used": lac_year or wld_year or "N/A",
        })

    # Guardar CSV
    output_path = os.path.abspath(OUTPUT_FILE)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["indicator", "LAC", "WLD", "downloaded", "year_used"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nGuardado en: {output_path}")
    print(f"Filas: {len(rows)} | Columnas: indicator, LAC, WLD, downloaded, year_used")

    nulls = [r["indicator"] for r in rows if r["LAC"] is None or r["WLD"] is None]
    if nulls:
        print(f"\nADVERTENCIA: Valores nulos en: {nulls}")
        print("El dashboard usará la API en vivo como respaldo para esos indicadores.")
    else:
        print("\nTodos los valores descargados correctamente.")


if __name__ == "__main__":
    main()
