#!/bin/bash

echo "======================================"
echo "  Launching Django Project HELBAgent"
echo "======================================"

echo "📦 Installing Python dependencies..."

python3 -m pip install --upgrade pip
pip install -r requirements.txt

cd HELBAgent
echo " Starting Django server..."
echo " Applying database migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

echo ""
echo "=========================================="
echo "✅ Server is starting..."
echo "=========================================="
echo ""
echo "🌐 Access the application at:"
echo "   http://127.0.0.1:8000"
xdg-open "http://127.0.0.1:8000" >/dev/null 2>&1 &
python3 manage.py runserver