from fastapi import FastAPI, HTTPException, status

from app.models import ServiceRequest, ServiceRequestCreate
from app.storage import create_request, get_request, list_requests


app = FastAPI(
    title="Service Intake API",
    description=(
        "A multilingual API for receiving and managing "
        "home maintenance service requests."
    ),
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/requests",
    response_model=ServiceRequest,
    status_code=status.HTTP_201_CREATED,
)
def submit_request(data: ServiceRequestCreate) -> ServiceRequest:
    return create_request(data)


@app.get(
    "/requests",
    response_model=list[ServiceRequest],
)
def read_requests() -> list[ServiceRequest]:
    return list_requests()


@app.get(
    "/requests/{request_id}",
    response_model=ServiceRequest,
)
def read_request(request_id: int) -> ServiceRequest:
    service_request = get_request(request_id)

    if service_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found",
        )

    return service_request