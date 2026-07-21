from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session

from app.database import create_db_and_tables, get_session
from app.models import (
    ServiceRequest,
    ServiceRequestCreate,
    ServiceRequestRecord,
    ServiceRequestStatusUpdate,
)
from app.storage import (
    create_request,
    get_request,
    list_requests,
    update_request_status,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    create_db_and_tables()
    yield


app = FastAPI(
    title="Service Intake API",
    description=(
        "A multilingual API for receiving and managing "
        "home maintenance service requests."
    ),
    version="0.2.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/requests",
    response_model=ServiceRequest,
    status_code=status.HTTP_201_CREATED,
)
def submit_request(
    data: ServiceRequestCreate,
    session: Session = Depends(get_session),
) -> ServiceRequestRecord:
    return create_request(
        session=session,
        data=data,
    )


@app.get(
    "/requests",
    response_model=list[ServiceRequest],
)
def read_requests(
    session: Session = Depends(get_session),
) -> list[ServiceRequestRecord]:
    return list_requests(session=session)


@app.get(
    "/requests/{request_id}",
    response_model=ServiceRequest,
)
def read_request(
    request_id: int,
    session: Session = Depends(get_session),
) -> ServiceRequestRecord:
    service_request = get_request(
        session=session,
        request_id=request_id,
    )

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
    session: Session = Depends(get_session),
) -> ServiceRequestRecord:
    service_request = update_request_status(
        session=session,
        request_id=request_id,
        new_status=data.status,
    )

    if service_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found",
        )

    return service_request