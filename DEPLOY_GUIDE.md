# Geo-Ciencia 360 — Guía de Deployment

## Primera vez (setup completo)

### 1. Instalar dependencias
```
cd C:\Users\libra\Documents\HACKODS\hackods
venv\Scripts\activate
pip install ghp-import
```

### 2. Inicializar Git y conectar a GitHub
```
git init
git add -A
git commit -m "init geo-ciencia-360"
git branch -M main
git remote add origin https://github.com/libradito/geo-ciencia-360.git
git push -u origin main
```

### 3. Render el dashboard
```
$env:QUARTO_PYTHON="venv/Scripts/python.exe"
quarto render dashboard.qmd
```

### 4. Deploy a GitHub Pages
```
ghp-import -n -p -f _site
```

### 5. Activar GitHub Pages
- Ve a: https://github.com/libradito/geo-ciencia-360/settings/pages
- Source: branch `gh-pages`, folder `/ (root)`
- Click **Save**
- URL: **https://libradito.github.io/geo-ciencia-360/**

---

## Cada vez que hagas cambios

```
venv\Scripts\activate
$env:QUARTO_PYTHON="venv/Scripts/python.exe"
quarto render dashboard.qmd
git add -A
git commit -m "update dashboard"
git push origin main
ghp-import -n -p -f _site
```

O simplemente corre `deploy.bat`

---

## Troubleshooting

| Problema | Solución |
|----------|----------|
| `quarto: not recognized` | Instalar Quarto: https://quarto.org/docs/get-started/ y reiniciar terminal |
| `jupyter-cache required` | Ya lo arreglamos: el dashboard usa `cache: false` |
| `ghp-import: not recognized` | `pip install ghp-import` |
| Mapa no carga | Normal — usa Plotly built-in geography, no necesita GeoJSON externo |
| CONEVAL data missing | Bajar CSV de https://www.coneval.org.mx/Medicion/Paginas/Programas_BD_municipal_2010_2020.aspx y ponerlo en `data/` |
| API World Bank no responde | El dashboard muestra "N/D" y sigue funcionando — try/except en todo |

---

## Archivos clave

- `dashboard.qmd` — El dashboard (lo que editas)
- `modules/core.py` — La función `get_ods_data()` que jala todo
- `modules/coneval.py` — Datos CONEVAL local
- `modules/inegi.py` — API INEGI (token incluido)
- `modules/worldbank.py` — API Banco Mundial (abierta)
- `_site/` — Output renderizado (lo que se publica)
- `styles.css` — Estilos visuales
