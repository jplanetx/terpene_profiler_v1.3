#!/bin/bash

echo "🧬 StrainMatch Pro - Enhanced Terpene Profiler"
echo "=============================================="
echo ""

# Make sure we're on the right branch
echo "📥 Pulling latest changes..."
git checkout claude/enhance-terpene-profiler-S2MDi
git pull origin claude/enhance-terpene-profiler-S2MDi

echo ""
echo "✅ All changes loaded!"
echo ""
echo "🚀 Launching Streamlit app..."
echo "   Your browser will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the app"
echo "=============================================="

# Launch the app
streamlit run app.py
