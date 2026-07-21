from fastapi import FastAPI, HTTPException, status

from app.models import (
    ServiceRequest,
    ServiceRequestCreate,
    ServiceRequestStatusUpdate,
)

from app.storage import (
    create_request,
    get_request,
    list_requests,
    update_request_status,
)

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

@app.patch(
    "/requests/{request_id}/status",
    response_model=ServiceRequest,
)
def change_request_status(
    request_id: int,
    data: ServiceRequestStatusUpdate,
) -> ServiceRequest:
    service_request = update_request_status(
        request_id=request_id,
        new_status=data.status,
    )

    if service_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found",
        )

    return service_request