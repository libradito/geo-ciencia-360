# Geo-Ciencia 360

Dashboard interactivo que compara indicadores de **San Juan Chamula, Chiapas** contra promedios nacionales, regionales (LATAM) y mundiales, alineados a los Objetivos de Desarrollo Sostenible (ODS) 1, 4, 5 y 8.

**Equipo HackODS UNAM 2026 — Empoderando Arte**

## Estructura del Proyecto

```
geo-ciencia-360/
├── modules/
│   ├── __init__.py
│   ├── coneval.py        # Datos CONEVAL (pobreza municipal)
│   ├── inegi.py          # API INEGI (indicadores estatales)
│   ├── worldbank.py      # API Banco Mundial (LATAM + Mundo)
│   └── core.py           # Integración + auditoría
├── data/
│   └── coneval_pobreza_municipal.xlsx
├── dashboard.qmd         # Dashboard Quarto
├── styles.css            # Estilos del dashboard
├── _quarto.yml           # Configuración Quarto
├── requirements.txt      # Dependencias Python
├── README.md
└── .gitignore
```

## Fuentes de Datos

| Fuente | Tipo | Datos |
|--------|------|-------|
| CONEVAL | Excel local | Pobreza municipal 2020 (2,469 municipios) |
| INEGI | API con token | Indicadores estatales Chiapas |
| Banco Mundial | API abierta | Indicadores LATAM y mundiales |
| ONU | Referencia | Custodio oficial de indicadores ODS |

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
quarto render dashboard.qmd
```

## Equipo

Geo-Ciencia 360 — HackODS UNAM 2026 — Empoderando Arte
