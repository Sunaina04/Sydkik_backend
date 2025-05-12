#!/bin/bash
# Wait for the database to be ready before running the migrations and starting the app
# echo "Waiting for the database to be ready..."
# sleep 10  # You can adjust this depending on how long it takes for your database to start

# # Run Alembic migrations
# echo "Applying Alembic migrations..."
# alembic upgrade head

# Start the application (Uvicorn for FastAPI)
echo "Starting the application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
