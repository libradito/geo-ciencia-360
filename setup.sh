#!/bin/bash
# ─── HackODS Project Setup ───────────────────────────────────────────
# Run this script once to create the virtual environment and install
# all dependencies needed for the dashboard.
#
# Usage:
#   chmod +x setup.sh
#   ./setup.sh
# ─────────────────────────────────────────────────────────────────────

set -e

echo "🚀 HackODS — Setting up project environment..."
echo ""

# ── Step 1: Create virtual environment ───────────────────────────────
if [ -d "venv" ]; then
    echo "✅ Virtual environment already exists."
else
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created."
fi

# ── Step 2: Activate it ──────────────────────────────────────────────
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# ── Step 3: Upgrade pip ──────────────────────────────────────────────
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# ── Step 4: Install dependencies ─────────────────────────────────────
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt --quiet

# ── Step 5: Verify installation ──────────────────────────────────────
echo ""
echo "🔍 Verifying installed packages..."
pip list | grep -E "pandas|geopandas|plotly|requests|openpyxl|shapely"

# ── Step 6: Freeze exact versions ────────────────────────────────────
pip freeze > requirements-lock.txt
echo ""
echo "🔒 Locked versions saved to requirements-lock.txt"

# ── Step 7: Verify data file ────────────────────────────────────────
echo ""
if [ -f "data/coneval_pobreza_municipal.csv" ] || [ -f "data/coneval_pobreza_municipal.xlsx" ]; then
    echo "✅ CONEVAL data file found."
else
    echo "⚠️  CONEVAL data file missing!"
    echo "   Download from: https://www.coneval.org.mx/Medicion/Paginas/Programas_BD_municipal_2010_2020.aspx"
    echo "   Save as: data/coneval_pobreza_municipal.csv"
fi

# ── Step 8: Quick test ───────────────────────────────────────────────
echo ""
echo "🧪 Running quick data test..."
python3 -c "
from modules.coneval import load_coneval_data, get_chamula_value, _find_column
df = load_coneval_data()
if df is not None:
    val = get_chamula_value(df, 'pobreza_e')
    if val:
        print(f'   Chamula pobreza extrema: {val}%')
        print('   ✅ Data engine working!')
    else:
        print('   ⚠️  Data loaded but Chamula not found. Check column names.')
else:
    print('   ❌ Could not load CONEVAL data. Check the data/ folder.')
"

# ── Step 9: Download World Bank cache ────────────────────────────────
echo ""
if [ -f "data/wb_cache.csv" ]; then
    echo "✅ World Bank cache already exists. Skipping download."
    echo "   To refresh: python scripts/download_wb_cache.py"
else
    echo "🌐 Downloading World Bank indicators (LAC + World)..."
    python3 scripts/download_wb_cache.py
fi

# ── Done ─────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✅ Setup complete!"
echo ""
echo "  To activate the environment:"
echo "    source venv/bin/activate"
echo ""
echo "  To render the dashboard:"
echo "    quarto render dashboard.qmd"
echo ""
echo "  To preview live:"
echo "    quarto preview dashboard.qmd"
echo ""
echo "  To refresh World Bank data (annually):"
echo "    python scripts/download_wb_cache.py"
echo "════════════════════════════════════════════════════════════"
