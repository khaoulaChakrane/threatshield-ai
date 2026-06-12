from pydantic import BaseModel
from datetime import datetime

class URLScanRequest(BaseModel):
    url: str

class ScanResultResponse(BaseModel):
    id: int
    scan_type: str
    target: str
    verdict: str
    risk_score: float
    created_at: datetime

    class Config:
        from_attributes = True