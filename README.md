# ThreatShield AI
### Plateforme Web de Détection de Menaces Cybersécurité

![Status](https://img.shields.io/badge/Status-En%20développement-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green)
![React](https://img.shields.io/badge/React-18-61dafb)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)

## Description
ThreatShield AI est une plateforme full-stack de détection de menaces
qui analyse URLs, emails, domaines, fichiers et adresses IP pour
identifier les cybermenaces en temps réel.

## Stack Technique
| Couche | Technologie |
|--------|------------|
| Frontend | React 18, Vite, Axios |
| Backend | Python 3.12, FastAPI |
| Base de données | PostgreSQL 16, SQLAlchemy |
| Authentification | JWT, bcrypt |
| ML | scikit-learn, XGBoost, SHAP |
| DevOps | Docker, GitHub Actions |

## Fonctionnalités
- [ ] Authentification JWT (register/login)
- [ ] Scan d'URLs (VirusTotal API)
- [ ] Analyse d'emails
- [ ] Vérification de domaines (WHOIS)
- [ ] Scan de fichiers (hash + antivirus)
- [ ] Vérification IP (AbuseIPDB)
- [ ] Dashboard avec historique
- [ ] Modèle ML de classification
- [ ] Déploiement Docker

## Installation locale

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Documentation API
Swagger disponible sur : http://localhost:8001/docs

## Auteure
**khaoula Chakrane** — [GitHub](https://github.com/khaoulaChakrane)