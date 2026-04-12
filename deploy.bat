@echo off
REM ─── Geo-Ciencia 360 — Deploy to GitHub Pages ─────────────────────
REM Run this after making changes to re-render and publish.
REM
REM Prerequisites:
REM   - Git initialized and remote set
REM   - ghp-import installed (pip install ghp-import)
REM   - Quarto installed
REM ────────────────────────────────────────────────────────────────────

echo.
echo  Geo-Ciencia 360 — Build and Deploy
echo  ====================================
echo.

REM ── Activate venv ──────────────────────────────────────────────────
call venv\Scripts\activate.bat

REM ── Set Python for Quarto ──────────────────────────────────────────
set QUARTO_PYTHON=venv\Scripts\python.exe

REM ── Render dashboard ───────────────────────────────────────────────
echo  [1/3] Rendering dashboard...
quarto render dashboard.qmd
if errorlevel 1 (
    echo  ERROR: Quarto render failed!
    pause
    exit /b 1
)
echo  Dashboard rendered successfully.

REM ── Commit changes ─────────────────────────────────────────────────
echo.
echo  [2/3] Committing changes...
git add -A
git commit -m "update dashboard"
git push origin main

REM ── Deploy to GitHub Pages ─────────────────────────────────────────
echo.
echo  [3/3] Deploying to GitHub Pages...
ghp-import -n -p -f _site
if errorlevel 1 (
    echo  ERROR: Deploy failed! Make sure ghp-import is installed:
    echo    pip install ghp-import
    pause
    exit /b 1
)

echo.
echo  ============================================================
echo   Deploy complete!
echo   Your dashboard is live at:
echo   https://YOUR_USERNAME.github.io/geo-ciencia-360/
echo  ============================================================
echo.
pause
