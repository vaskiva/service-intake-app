from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class Language(str, Enum):
    FI = "fi"
    SV = "sv"
    EN = "en"


class Category(str, Enum):
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"
    ROOFING = "roofing"
    GENERAL_MAINTENANCE = "general_maintenance"


class RequestStatus(str, Enum):
    RECEIVED = "received"
    REVIEWING = "reviewing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ServiceRequestCreate(BaseModel):
    language: Language
    category: Category

    description: str = Field(
        min_length=10,
        max_length=2000,
    )

    postal_code: str = Field(
        pattern=r"^\d{5}$",
    )

    customer_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr


class ServiceRequest(ServiceRequestCreate):
    id: int
    status: RequestStatus