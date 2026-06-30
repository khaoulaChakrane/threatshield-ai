from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.dependencies import get_current_user
from app.models.user import User
from app.ml.predictor import predict_url

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])

class MLPredictRequest(BaseModel):
    url: str

@router.post("/predict")
def ml_predict(
    payload: MLPredictRequest,
    current_user: User = Depends(get_current_user)
):
    result = predict_url(payload.url)
    return result