FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Alembic for migrations
RUN pip install alembic

COPY . .