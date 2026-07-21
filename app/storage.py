from sqlmodel import Session, select

from app.models import (
    RequestStatus,
    ServiceRequestCreate,
    ServiceRequestRecord,
)


def create_request(
    session: Session,
    data: ServiceRequestCreate,
) -> ServiceRequestRecord:
    service_request = ServiceRequestRecord(
        **data.model_dump(),
        status=RequestStatus.RECEIVED,
    )

    session.add(service_request)
    session.commit()
    session.refresh(service_request)

    return service_request


def list_requests(
    session: Session,
) -> list[ServiceRequestRecord]:
    statement = select(ServiceRequestRecord)

    return list(session.exec(statement).all())


def get_request(
    session: Session,
    request_id: int,
) -> ServiceRequestRecord | None:
    return session.get(ServiceRequestRecord, request_id)


def update_request_status(
    session: Session,
    request_id: int,
    new_status: RequestStatus,
) -> ServiceRequestRecord | None:
    service_request = session.get(
        ServiceRequestRecord,
        request_id,
    )

    if service_request is None:
        return None

    service_request.status = new_status

    session.add(service_request)
    session.commit()
    session.refresh(service_request)

    return service_request