#!/bin/bash
# Setup script for Regression Exam Prep
# Run once: bash setup.sh

echo "🔧 Setting up Regression Exam Prep..."

cd "$(dirname "$0")"

# Create venv with stable Python using uv
uv venv --python 3.12 .venv
source .venv/bin/activate

# Install dependencies
uv pip install streamlit plotly pandas

echo ""
echo "✅ Setup complete!"
echo "Run the app with: yakir"
echo ""