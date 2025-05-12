# Using Python 3.11 slim image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run Alembic migrations and start app (done via entrypoint.sh script)
ENTRYPOINT ["./entrypoint.sh"]
