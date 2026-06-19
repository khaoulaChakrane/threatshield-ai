from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class URLScanRequest(BaseModel):
    url: str

class ScanResultResponse(BaseModel):
    id: int
    scan_type: str
    target: str
    verdict: str
    risk_score: float
    created_at: datetime
    details: Optional[str] = None

    class Config:
        from_attributes = True

class IPScanRequest(BaseModel):
    ip: str

class DomainScanRequest(BaseModel):
    domain: str