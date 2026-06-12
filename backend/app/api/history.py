from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.scan_result import ScanResult
from app.schemas.scan import ScanResultResponse

router = APIRouter(prefix="/api/history", tags=["Historique"])

@router.get("/", response_model=List[ScanResultResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scans = (
        db.query(ScanResult)
        .filter(ScanResult.user_id == current_user.id)
        .order_by(ScanResult.created_at.desc())
        .all()
    )
    return scans

@router.get("/{scan_id}", response_model=ScanResultResponse)
def get_scan_detail(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scan = (
        db.query(ScanResult)
        .filter(ScanResult.id == scan_id, ScanResult.user_id == current_user.id)
        .first()
    )
    if not scan:
        raise HTTPException(status_code=404, detail="Scan introuvable")
    return scan