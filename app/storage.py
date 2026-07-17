from app.models import (
    RequestStatus,
    ServiceRequest,
    ServiceRequestCreate,
)


_requests: list[ServiceRequest] = []
_next_id = 1


def create_request(data: ServiceRequestCreate) -> ServiceRequest:
    global _next_id

    service_request = ServiceRequest(
        id=_next_id,
        status=RequestStatus.RECEIVED,
        **data.model_dump(),
    )

    _requests.append(service_request)
    _next_id += 1

    return service_request


def list_requests() -> list[ServiceRequest]:
    return _requests.copy()


def get_request(request_id: int) -> ServiceRequest | None:
    for service_request in _requests:
        if service_request.id == request_id:
            return service_request

    return None