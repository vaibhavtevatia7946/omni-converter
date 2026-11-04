#!/bin/bash
# Script to launch OmniConvert Web Application

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

echo "=========================================================="
echo "🚀 Starting OmniConvert - Universal All-in-One Converter"
echo "🌐 Open your browser at: http://127.0.0.1:8000"
echo "=========================================================="

./venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --reload
