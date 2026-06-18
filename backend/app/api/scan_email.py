import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.scan_result import ScanResult
from app.schemas.scan import ScanResultResponse
from app.services.email_service import analyze_email

router = APIRouter(prefix="/api/scan", tags=["Scan"])

@router.post("/email", response_model=ScanResultResponse)
async def scan_email_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contents = await file.read()

    try:
        result = analyze_email(contents, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur d'analyse: {str(e)}")

    scan = ScanResult(
        user_id=current_user.id,
        scan_type="email",
        target=result["subject"] or file.filename,
        verdict=result["verdict"],
        risk_score=result["risk_score"],
        details=json.dumps(result)
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan