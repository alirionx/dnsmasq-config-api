import socket
import uuid
import ipaddress
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class ApiStatus(BaseModel):
    timestamp: datetime | None = datetime.now()
    method: Literal["GET", "POST", "PUT", "DELETE"]
    hostname: str | None = socket.gethostname()
    base_url: str | None = None
    url_path: str | None = None
    message: str | None = None


class SystemdStatus(BaseModel):
    name: str
    enabled: bool
    running: bool


class HostRecord(BaseModel):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4)
    hostnames: list[str] 
    ipv4_address: ipaddress.IPv4Address 
    ipv6_address: ipaddress.IPv6Address | None = None


