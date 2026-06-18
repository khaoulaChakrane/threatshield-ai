import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.scan_result import ScanResult
from app.schemas.scan import ScanResultResponse
from app.services.file_service import scan_file as analyze_file

router = APIRouter(prefix="/api/scan", tags=["Scan"])

MAX_FILE_SIZE = 30 * 1024 * 1024  # 30 MB

@router.post("/file", response_model=ScanResultResponse)
async def scan_file_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Fichier trop volumineux (max 30MB)")

    try:
        result = analyze_file(contents, file.filename)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur VirusTotal: {str(e)}")

    scan = ScanResult(
        user_id=current_user.id,
        scan_type="file",
        target=f"{file.filename} ({result['sha256'][:12]}...)",
        verdict=result["verdict"],
        risk_score=result["risk_score"],
        details=json.dumps(result)
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan