import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.scan_result import ScanResult
from app.schemas.scan import IPScanRequest, ScanResultResponse
from app.services.ip_service import scan_ip as analyze_ip

router = APIRouter(prefix="/api/scan", tags=["Scan"])

@router.post("/ip", response_model=ScanResultResponse)
def scan_ip_endpoint(
    payload: IPScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        result = analyze_ip(payload.ip)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur AbuseIPDB: {str(e)}")

    scan = ScanResult(
        user_id=current_user.id,
        scan_type="ip",
        target=payload.ip,
        verdict=result["verdict"],
        risk_score=result["risk_score"],
        details=json.dumps(result)
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan