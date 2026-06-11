from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.auth import router as auth_router  


# Crée les tables automatiquement
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ThreatShield AI",
    description="Plateforme de détection de menaces",
    version="1.0.0"
)
app.include_router(auth_router)                


# Autorise React (localhost:5173) à parler à FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "ThreatShield AI is running 🛡️"}

@app.get("/health")
def health():
    return {"status": "ok"}