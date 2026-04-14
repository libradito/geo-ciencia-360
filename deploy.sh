#!/bin/bash
# ─── HackODS — Deploy to GitHub Pages (Mac/Linux) ────────────────────
# Run this after making changes to re-render and publish.
#
# Prerequisites:
#   - Git initialized and remote set
#   - ghp-import installed (pip install ghp-import)
#   - Quarto installed
#
# Usage:
#   chmod +x deploy.sh
#   ./deploy.sh
# ─────────────────────────────────────────────────────────────────────

set -e

echo ""
echo " HackODS — Build and Deploy"
echo " ============================"
echo ""

# ── Activate venv ─────────────────────────────────────────────────────
source venv/bin/activate

# ── Set Python for Quarto ─────────────────────────────────────────────
export QUARTO_PYTHON=venv/bin/python

# ── Step 1: Render dashboard ──────────────────────────────────────────
echo " [1/3] Rendering dashboard..."
quarto render dashboard.qmd
echo " Dashboard rendered successfully."

# ── Step 1b: Cache-bust styles.css ───────────────────────────────────
echo ""
echo " [1b] Cache-busting CSS..."
python cache_bust.py || echo " WARNING: cache_bust.py failed — CSS may not refresh in browsers"

# ── Step 2: Commit changes ────────────────────────────────────────────
echo ""
echo " [2/3] Committing changes..."
git add -A
git commit -m "update dashboard"
git push origin main

# ── Step 3: Deploy to GitHub Pages ───────────────────────────────────
echo ""
echo " [3/3] Deploying to GitHub Pages..."
ghp-import -n -p -f _site

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  Deploy complete!"
echo "  Your dashboard is live at:"
echo "  https://YOUR_USERNAME.github.io/hackods/"
echo "════════════════════════════════════════════════════════════"
echo ""
