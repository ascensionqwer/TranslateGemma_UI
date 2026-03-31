#!/bin/bash
# TranslateGemma Translator - One-Click Launch Script
# This script starts the Flask server and opens the translator in your browser

echo "=============================================="
echo "  TranslateGemma Translator Launcher"
echo "=============================================="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    echo "   Download from: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if Ollama is running
echo ""
echo "Checking if Ollama is running..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama is running"
    
    # Check if translategemma:27b model is available
    if curl -s http://localhost:11434/api/tags | grep -q "translategemma"; then
        echo "✓ TranslateGemma model is available"
    else
        echo "⚠ TranslateGemma model not found. Pulling the model..."
        echo "   This may take a few minutes..."
        ollama pull translategemma:27b
    fi
else
    echo "❌ Ollama is not running. Please start Ollama first."
    echo "   Run: ollama serve"
    echo "   Or download Ollama from: https://ollama.com"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
echo ""
echo "Checking dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Start the Flask server
echo ""
echo "=============================================="
echo "  Starting TranslateGemma Translator..."
echo "=============================================="
echo ""
echo "Server will run at: http://localhost:5001"
echo "(Port 5001 used to avoid macOS AirPlay Receiver conflict)"
echo "Press Ctrl+C to stop the server"
echo ""

# Open browser after a short delay
sleep 2 && open "http://localhost:5001" &

# Start Flask app
python3 app.py