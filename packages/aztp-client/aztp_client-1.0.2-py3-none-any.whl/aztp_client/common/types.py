from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Identity(BaseModel):
    spiffe_id: str
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Metadata(BaseModel):
    hostname: str
    environment: str
    extra: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class IssueIdentityRequest(BaseModel):
    workload_id: str
    agent_id: str
    timestamp: str
    method: str
    metadata: Metadata

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SecuredAgent(BaseModel):
    name: str
    identity: Optional[Identity] = None
    metadata: Optional[Metadata] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 