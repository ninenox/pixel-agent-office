#!/bin/bash
cd "$(dirname "$0")"
echo "Starting Claude Agent Office backend..."
echo "Open http://localhost:19000"
python3 app.py
