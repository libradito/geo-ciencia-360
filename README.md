#🌍Geo-Ciencia 360 — Empoderando Arte
Más de **38,000 mujeres indígenas artesanas y campesinas** en San Juan Chamula, Chiapas, viven en una intersección crítica de pobreza, desigualdad y falta de acceso a educación y empleo digno.

Objetivo del proyecto.
Evidenciar con un tablero de ciencia de datos, la realidad de los pueblos originarios de Mexico, para generar una propuesta de solución práctica, viable y replicable.
Este proyecto cruza **más de dos años de evidencia de campo** con **ciencia de datos oficial y auditable** para visibilizar una brecha estructural profunda en los Objetivos de Desarrollo Sostenible:
- **ODS 1 — Fin de la pobreza**
- **ODS 4 — Educación de calidad**
- **ODS 5 — Igualdad de género**
- **ODS 8 — Trabajo decente y crecimiento económico**
El resultado no es solo un diagnóstico; es una llamada urgente a la acción.
---
# 💡 De la evidencia en datos a la solución.
Geo-Ciencia 360 no se detiene en mostrar el problema.
Conecta directamente con una solución real, práctica, disruptiva, activa y replicable:
## **Empoderando Arte** https://www.empoderandoarte.com/ 
Una plataforma diseñada para que artesanas de pueblos originarios —incluso aquellas que no hablan español— puedan:
- Comercializar sus productos en su **lengua materna**
- Conectarse con clientes en **cualquier parte del mundo**
- Romper barreras estructurales de acceso al mercado digital**
- Vender sin intermediarios y obtener el pago justo por su trabajo**
---
### 🌐 Impacto escalable
Este proyecto propone un modelo práctico y replicable que puede extenderse:
- A nivel **regional (LATAM)**
- A nivel **global**
Contribuyendo directamente al cumplimiento de la **Agenda 2030 de los ODS**.
---
#### 🤝 Llamado a la acción
Te invitamos a explorar, compartir y a sumarte para amplificar este proyecto.
Porque detrás de cada dato, hay una historia y detrás de cada historia, hay una oportunidad de cambio.
Apoyar este proyecto es contribuir a:
- Reducir desigualdades estructurales  
- Impulsar economías locales  
- Construir un futuro más justo  
---
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
#####👥 Equipo
**Geo-Ciencia 360 — mentes y manos en acción para crear un mundo mejor**
- Daniel Bueno Córdoba — Líder  
- Librado Hernandez Cruz — Tecnología  
- Edith Liera Maciel — Finanzas 




