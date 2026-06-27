#!/bin/bash
# Setup script for AI Assistant feature
# Run this once to install dependencies and build the vector store

echo "=========================================="
echo "🤖 AI Assistant Setup - רגרסיה לינארית"
echo "=========================================="

# Navigate to project directory
cd "$(dirname "$0")"

echo ""
echo "📦 Step 1: Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "🧠 Step 2: Building vector store from course documents..."
echo "   This may take a few minutes (downloading embedding model + indexing documents)..."
python data/build_vector_store.py

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo ""
echo "To start the app:"
echo "  streamlit run app.py"
echo ""
echo "To configure the AI proxy URL, edit .env file:"
echo "  AI_PROXY_URL=http://localhost:8080/v1"
echo "=========================================="