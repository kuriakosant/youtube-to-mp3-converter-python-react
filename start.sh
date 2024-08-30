#!/bin/bash
#This is a bash start script , if you arent sure how to use it please read the readme file

# Navigate to the backend and start it
echo "Starting backend..."
cd backend
source venv/bin/activate  # Activate the virtual environment
python app.py &  # Run backend in the background
BACKEND_PID=$!  # Capture backend process ID
cd ..

# Navigate to the frontend and start it
echo "Starting frontend..."
cd frontend
npm start &  # Run frontend in the background
FRONTEND_PID=$!  # Capture frontend process ID

# Instruction for quitting
echo "Both frontend and backend are running. To stop, press CTRL + C."

# Wait for processes to be stopped (Ctrl + C will stop them)
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT

wait
