# Service Intake API

A multilingual FastAPI service for receiving and managing home maintenance service requests.

The project is an early prototype for a digital service intake system that could help small field service businesses receive clearer customer requests in Finnish.

## Current features

- Create a service request
- List all service requests
- Retrieve a service request by ID
- Validate customer input with Pydantic
- Categorize requests by service type
- Return appropriate HTTP status codes
- Docker Compose
- persistent Docker volume
- environment-based configuration
- container health check
- GitHub Actions CI

## Technology

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- Git
- SQLModel
- SQLAlchemy
- SQLite
- Docker 
- Docker Compose
- GitHub Actions

## Project structure

```text
service-intake-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── storage.py
├── data/
├── tests/
|── Dockerfile
|── .dockerignore
|── compose.yaml 
├── .gitignore
├── README.md
└── requirements.txt
```

## Local development setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/service-intake-api.git
cd service-intake-api
```

Replace `YOUR_USERNAME` with the correct GitHub username.

### 2. Create a virtual environment

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start the development server

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check whether the API is running |
| POST | `/requests` | Create a service request |
| GET | `/requests` | List all service requests |
| GET | `/requests/{request_id}` | Retrieve one service request |

## Example request

```json
{
  "language": "en",
  "category": "plumbing",
  "description": "Water is leaking under the kitchen sink.",
  "postal_code": "10300",
  "customer_name": "Tiina Smith",
  "email": "tiina@example.com"
}
```

Example response:

```json
{
  "language": "en",
  "category": "plumbing",
  "description": "Water is leaking under the kitchen sink.",
  "postal_code": "10300",
  "customer_name": "Tiina Smith",
  "email": "tiina@example.com",
  "id": 1,
  "status": "received"
}
```
## Running with Docker

The API can be built and run locally using Docker Compose.

Start the application
docker compose up -d --build

Check that the service is running:

docker compose ps

Test the health endpoint:

curl http://localhost:8000/health

Expected response:

{"status":"ok"}

Interactive API documentation is available at:

http://localhost:8000/docs
View logs
docker compose logs -f api
Stop the application
docker compose down

## Data storage

The application uses SQLite for persistent storage.

When running locally without Docker, the database is stored in:

data/service_intake.db

When running in Docker, the database is stored inside the container at:

/app/data/service_intake.db

Docker Compose mounts a named Docker volume to /app/data:

service-intake-data

This separates persistent data from the container lifecycle. Containers can therefore be stopped, removed, and recreated without deleting submitted service requests.

For example:

docker compose down
docker compose up -d

The database remains available through the Docker volume.

docker compose down -v also removes the associated volume and should only be used when the stored data is intentionally being deleted.

The SQLite database file is excluded from Git version control.

## Running tests

Run the automated test suite from the project root:

```bash
python -m pytest -v
```
The current test suite covers:

API health checking
creating a valid service request
rejecting invalid request data
listing service requests
retrieving a request by ID
returning 404 for a missing request

## CI

- run tests
- validates Compose config
- builds and starts the app
- waits for healthcheck
- performs HTTP smoke test

## Production deployment

Production deployment is not implemented yet.

The planned deployment path is:

GitHub repository
        ↓
Docker image
        ↓
Docker Compose
        ↓
Raspberry Pi or Linux server
        ↓
Health monitoring and backups

Before production use, the project will still need:

authentication and authorization
secure configuration and secrets management
HTTPS
logging and monitoring
backups
database migration strategy
privacy and data-retention policies
deployment and update procedures

## Roadmap

- [x] Define Pydantic request models
- [x] Implement in-memory storage
- [x] Add basic FastAPI endpoints
- [x] Add automated tests
- [x] Add request status updates
- [x] Replace in-memory storage with SQLite 
- [ ] Evaluate PostgreSQL for a later production deployment
- [x] Add Docker support
- [X] Add Docker compose
- [x] Add persistent docker storage
- [x] Add container health check
- [x] Configure application settings with environment variables
- [x] Add GitHub Actions CI
- [ ] Deploy to a Raspberry Pi / Linux server
- [ ] Add an AI-assisted request classification workflow

## Project status

Early development prototype.

The current version includes:

REST API built with FastAPI
validated request models
SQLite persistence
request status updates
automated tests
Docker image
Docker Compose configuration
persistent Docker volume

The application is suitable for local development and testing, but is not yet intended for production use.