from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.history import router as history_router
from app.api.scan_ip import router as scan_ip_router    
from app.api.scan_domain import router as scan_domain_router
from app.api.scan_file import router as scan_file_router    
from app.models.user import User
from app.models.scan_result import ScanResult

from app.api.auth import router as auth_router
from app.api.scan_url import router as scan_url_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ThreatShield AI",
    description="Plateforme de détection de menaces",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(scan_url_router)
app.include_router(history_router)
app.include_router(scan_ip_router) 
app.include_router(scan_domain_router)    
app.include_router(scan_file_router)                        

@app.get("/")
def root():
    return {"message": "ThreatShield AI is running "}

@app.get("/health")
def health():
    return {"status": "ok"}