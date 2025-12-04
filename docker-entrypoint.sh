#!/bin/bash

echo "🔍 Starting VECTOR Product Research Agent"
echo "========================================"

# Start FastAPI in the background
echo "🚀 Starting FastAPI server on port 8000..."
/app/.venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Wait a moment for FastAPI to start
sleep 5

# Start Streamlit
echo "🎨 Starting Streamlit app on port 8501..."
/app/.venv/bin/streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501 &
STREAMLIT_PID=$!

# Wait for any process to exit
wait $FASTAPI_PID $STREAMLIT_PID

# Exit with status of process that exited first
exit $?