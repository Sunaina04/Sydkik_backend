# sidekik Backend

This is the backend of the **sidekik** application built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. The project is containerized using **Docker**, and authentication is provided through **Google OAuth**.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Docker Setup](#docker-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [License](#license)

## Installation

### Prerequisites

Ensure you have the following tools installed on your machine:

- **Docker** (for containerization)
- **Docker Compose** (for orchestrating multi-container applications)
- **Python 3.11** (if you prefer to run locally without Docker)

### Clone the Repository

To clone the project:

```bash
git clone https://github.com/Sunaina04/Sydkik_backend.git
cd Sydkik_backend
````

### Install Dependencies Locally (Optional)

If you prefer to run the project locally without Docker, follow these steps:

1. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:

   * On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

   * On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

3. **Install the Required Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Before running the application, you need to configure environment variables.

### Step 1: Create `.env` File

Copy the example file:

```bash
cp .env.example .env
```

📝 After copying, open `.env` and update it with your actual database credentials and OAuth secrets.

### Step 2: Edit `.env`

```bash
# Database Configuration
DATABASE_USER=postgres
DATABASE_PASSWORD=securepassword
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=sidekik_db

# Application Secret Key (for session management)
SECRET_KEY=supersecretkey123

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

* Replace `your-google-client-id` and `your-google-client-secret` with your actual credentials from the [Google Developer Console](https://console.developers.google.com/).

---

## Docker Setup

This project uses **Docker** to containerize the application and its dependencies. With Docker, you can run and deploy the application without worrying about environment setup.

### Build and Start the Containers

To build and start the application containers (including FastAPI and PostgreSQL), run:

```bash
docker-compose up --build -d
```

This command will:

* Build the Docker images defined in the `Dockerfile` and `docker-compose.yml` file
* Start the `sidekik-db` container (PostgreSQL)
* Start the `sidekik-api` container (FastAPI)

### Stop the Containers

To stop the running containers and remove them:

```bash
docker-compose down
```

### Check Running Containers

To check which containers are running:

```bash
docker ps
```

---

## Running the Application

Once the Docker containers are up and running, the FastAPI application should be available at:

* **API Base URL**: `http://localhost:8000`

### Health Check Endpoint

Verify the app is running:

```bash
GET http://localhost:8000/
```

Response:

```json
{
  "status": "running"
}
```

### Database Connection Test

Test the database connection:

```bash
GET http://localhost:8000/api/v1/auth/db-test
```

Response:

```json
{
  "status": "success",
  "message": "Database connection successful"
}
```

---

## API Documentation

Once the app is running, access the interactive API documentation:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

These pages provide a live interface to test and understand all available routes.

---

## Additional Notes

* **Docker Networking**: The `sidekik-db` (PostgreSQL) and `sidekik-api` (FastAPI) containers are linked via Docker network. The FastAPI app accesses the database using the `db` hostname.

* **Environment Variables**: Secrets like `SECRET_KEY` and OAuth credentials should be stored in the `.env` file and **never** committed to version control. Add `.env` to `.gitignore`.

---