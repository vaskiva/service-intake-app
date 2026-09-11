# Service Intake App

[![CI](https://github.com/vaskiva/service-intake-app/actions/workflows/ci.yaml/badge.svg)](https://github.com/vaskiva/service-intake-app/actions/workflows/ci.yaml)

A small FastAPI service built as an end-to-end DevOps and Platform Engineering portfolio project.

The application receives and stores home maintenance service requests. The domain is intentionally simple so the project can focus on the complete delivery path: API design, validation, automated testing, containerization, persistent storage, CI, multi-platform image publishing, and repeatable deployment.

## What this project demonstrates

| Capability | Implementation |
|---|---|
| Backend API | FastAPI, Pydantic validation, SQLModel and SQLite |
| Automated testing | Pytest coverage for health, validation, request flows and status updates |
| Containerization | Docker image running as a non-root user |
| Persistent data | SQLite stored in a named Docker volume |
| Continuous integration | Tests, Compose validation, container build, health wait and HTTP smoke test |
| Artifact publishing | AMD64 and ARM64 images published to GitHub Container Registry |
| Deployment | Separate production Compose configuration using immutable Git SHA tags |
| Runtime controls | Healthcheck, restart policy, localhost-only port binding and `no-new-privileges` |

## Delivery flow

1. Pull requests run the test-and-build CI job.
2. A successful merge to `main` builds `linux/amd64` and `linux/arm64` images.
3. GitHub Actions publishes `latest` and immutable `sha-<commit>` tags to GHCR.
4. The deployment host pulls a selected SHA-tagged image.
5. Docker Compose starts the service, attaches persistent storage and verifies container health.

Container images: [GitHub Container Registry](https://github.com/vaskiva/service-intake-app/pkgs/container/service-intake-app)

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Return API health status |
| `POST` | `/requests` | Create a validated service request |
| `GET` | `/requests` | List service requests |
| `GET` | `/requests/{request_id}` | Retrieve one request |
| `PATCH` | `/requests/{request_id}/status` | Update request status |

Interactive API documentation is available at `http://127.0.0.1:8000/docs` while the service is running.

## Run locally

Requirements: Git, Docker Engine and Docker Compose.

```bash
git clone https://github.com/vaskiva/service-intake-app.git
cd service-intake-app
docker compose up -d --build
```

Verify the deployment:

```bash
docker compose ps
curl --fail http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Stop the local development stack without deleting its data:

```bash
docker compose down
```

## Production-like deployment

`compose.prod.yaml` runs a pre-built GHCR image instead of building source code on the deployment host. The port is bound to `127.0.0.1`, so the unauthenticated API is not exposed to the LAN or public internet.

Create the host-specific deployment configuration:

```bash
cp .env.production.example .env.production
```

Set `IMAGE_TAG` in `.env.production` to an image created by the CI workflow:

```dotenv
IMAGE_TAG=sha-REPLACE_WITH_FULL_GIT_COMMIT_SHA
APP_PORT=8000
```

`.env.production` is ignored by Git. Deploy the selected version:

```bash
docker compose --env-file .env.production -f compose.prod.yaml pull
docker compose --env-file .env.production -f compose.prod.yaml up -d
```

Verify the running image and health status:

```bash
docker compose --env-file .env.production -f compose.prod.yaml ps
docker inspect --format='{{.Config.Image}}' "$(docker compose --env-file .env.production -f compose.prod.yaml ps -q api)"
docker inspect --format='{{.State.Health.Status}}' "$(docker compose --env-file .env.production -f compose.prod.yaml ps -q api)"
curl --fail http://127.0.0.1:8000/health
```

View logs:

```bash
docker compose --env-file .env.production -f compose.prod.yaml logs -f api
```

### Update and rollback

To update, replace `IMAGE_TAG` with a newer SHA tag and repeat `pull` and `up -d`. To roll back, restore a previously working SHA tag and run the same commands. The deployment is reproducible because it does not depend on the mutable `latest` tag.

### Persistent data

SQLite is stored at `/app/data/service_intake.db` inside the container and persisted in the `service-intake-prod_service-intake-data` named volume.

The persistence path has been verified by creating a request, removing the container, creating a new container from the GHCR image, and confirming that the request remained available.

```bash
# Preserves the named volume
docker compose --env-file .env.production -f compose.prod.yaml down

# Deletes the named volume and its SQLite data
docker compose --env-file .env.production -f compose.prod.yaml down -v
```

## Run tests

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
```

The test suite covers valid and invalid requests, listing and retrieving data, missing resources, status updates and the health endpoint.

## Project structure

```text
service-intake-app/
├── .github/workflows/ci.yaml
├── app/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── storage.py
├── tests/
├── Dockerfile
├── compose.yaml
├── compose.prod.yaml
├── .env.production.example
└── requirements.txt
```

## Current scope and next steps

This is a production-like deployment exercise, not a public production service. The current API has no authentication, authorization or HTTPS, and the SQLite database has no automated backup or migration workflow.

Next infrastructure-focused steps:

- deploy the same immutable ARM64 image to a Raspberry Pi or Linux server
- add database-aware readiness checking
- implement and test SQLite backup and restore
- add structured logs and basic metrics
- add authentication and a reverse proxy with HTTPS before any public exposure
- evaluate PostgreSQL and schema migrations for multi-user or multi-instance use
