from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scan_type = Column(String, nullable=False)   # "url", "email", "domain"...
    target = Column(String, nullable=False)      # l'URL/email/IP scannée
    verdict = Column(String, nullable=False)     # "benign" / "malicious"
    risk_score = Column(Float, nullable=False)   # 0 à 100
    details = Column(Text, nullable=True)        # JSON brut de la réponse
    created_at = Column(DateTime(timezone=True), server_default=func.now())