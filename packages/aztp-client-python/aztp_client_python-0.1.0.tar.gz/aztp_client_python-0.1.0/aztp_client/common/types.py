from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Identity(BaseModel):
    spiffe_id: str
    certificate: str
    private_key: str
    ca_certificate: str


class Metadata(BaseModel):
    hostname: str
    environment: str
    extra: Dict[str, Any] = Field(default_factory=dict)


class IssueIdentityRequest(BaseModel):
    workload_id: str
    agent_id: str
    timestamp: datetime
    method: str
    metadata: Metadata


class SecuredAgent(BaseModel):
    name: str
    identity: Optional[Identity] = None
    metadata: Optional[Metadata] = None 