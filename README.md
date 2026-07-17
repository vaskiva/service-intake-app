# Service Intake API

A multilingual FastAPI service for receiving and managing home maintenance service requests.

The project is an early prototype for a digital service intake system that could help small field service businesses receive clearer customer requests in Finnish, Swedish, and English.

## Current features

- Create a service request
- List all service requests
- Retrieve a service request by ID
- Validate customer input with Pydantic
- Support Finnish, Swedish, and English request languages
- Categorize requests by service type
- Return appropriate HTTP status codes

## Technology

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- Git

## Project structure

```text
service-intake-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── storage.py
├── tests/
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
  "customer_name": "John Smith",
  "email": "john@example.com"
}
```

Example response:

```json
{
  "language": "en",
  "category": "plumbing",
  "description": "Water is leaking under the kitchen sink.",
  "postal_code": "10300",
  "customer_name": "John Smith",
  "email": "john@example.com",
  "id": 1,
  "status": "received"
}
```

## Data storage

The current version stores service requests in memory.

All stored requests are lost when the application is restarted. Persistent database storage will be added later.

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

## Production deployment

Production deployment is not implemented yet.

The planned deployment path is:

```text
GitHub repository
        ↓
Docker image
        ↓
Docker Compose
        ↓
Raspberry Pi or Linux server
        ↓
Health monitoring and backups
```

Before production use, the project will need:

- persistent database storage
- authentication and authorization
- secure configuration management
- HTTPS
- automated tests
- logging and monitoring
- backups
- privacy and data-retention policies

## Roadmap

- [x] Define Pydantic request models
- [x] Implement in-memory storage
- [x] Add basic FastAPI endpoints
- [x] Add automated tests
- [ ] Add request status updates
- [ ] Replace in-memory storage with SQLite or PostgreSQL
- [ ] Add Docker support
- [ ] Deploy to a Raspberry Pi
- [ ] Add multilingual summaries
- [ ] Add an AI-assisted request classification workflow

## Project status

Early development prototype. Not ready for production use.