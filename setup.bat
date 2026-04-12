@echo off
REM ─── HackODS Project Setup (Windows) ───────────────────────────────
REM Run this script once to create the virtual environment and install
REM all dependencies needed for the dashboard.
REM
REM Usage: double-click or run in terminal:
REM   setup.bat
REM ────────────────────────────────────────────────────────────────────

echo.
echo  HackODS — Setting up project environment...
echo.

REM ── Step 1: Create virtual environment ─────────────────────────────
if exist "venv" (
    echo  Virtual environment already exists.
) else (
    echo  Creating virtual environment...
    python -m venv venv
    echo  Virtual environment created.
)

REM ── Step 2: Activate it ────────────────────────────────────────────
echo  Activating virtual environment...
call venv\Scripts\activate.bat

REM ── Step 3: Upgrade pip ────────────────────────────────────────────
echo  Upgrading pip...
pip install --upgrade pip --quiet

REM ── Step 4: Install dependencies ───────────────────────────────────
echo  Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM ── Step 5: Verify installation ────────────────────────────────────
echo.
echo  Verifying installed packages...
pip list | findstr /i "pandas geopandas plotly requests openpyxl shapely"

REM ── Step 6: Freeze exact versions ──────────────────────────────────
pip freeze > requirements-lock.txt
echo.
echo  Locked versions saved to requirements-lock.txt

REM ── Step 7: Verify data file ───────────────────────────────────────
echo.
if exist "data\coneval_pobreza_municipal.csv" (
    echo  CONEVAL data file found.
) else if exist "data\coneval_pobreza_municipal.xlsx" (
    echo  CONEVAL data file found.
) else (
    echo  WARNING: CONEVAL data file missing!
    echo    Download from: https://www.coneval.org.mx/Medicion/Paginas/Programas_BD_municipal_2010_2020.aspx
    echo    Save as: data\coneval_pobreza_municipal.csv
)

REM ── Step 8: Quick test ─────────────────────────────────────────────
echo.
echo  Running quick data test...
python -c "from modules.coneval import load_coneval_data, get_chamula_value; df = load_coneval_data(); val = get_chamula_value(df, 'pobreza_e') if df is not None else None; print(f'   Chamula pobreza extrema: {val}%%') if val else print('   Check data folder')"

REM ── Done ───────────────────────────────────────────────────────────
echo.
echo ============================================================
echo   Setup complete!
echo.
echo   To activate the environment:
echo     venv\Scripts\activate
echo.
echo   To render the dashboard:
echo     quarto render dashboard.qmd
echo.
echo   To preview live:
echo     quarto preview dashboard.qmd
echo ============================================================
echo.
pause
