from fastapi import APIRouter

from app.api.v1.routes import users, auth, social_auth, enterprise, coaches, events, competitions, training

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(social_auth.router, prefix="/auth/social", tags=["Social Auth — Apple / Google / Facebook"])
api_router.include_router(users.router, prefix="/users", tags=["Usuarios"])
api_router.include_router(enterprise.router, prefix="/enterprise", tags=["Empresa — Pausas Activas"])
api_router.include_router(coaches.router, prefix="/coaches", tags=["Coach"])
api_router.include_router(training.router, prefix="/training", tags=["Entrenamiento"])
api_router.include_router(events.router, prefix="/events", tags=["Social — Eventos"])
api_router.include_router(competitions.router, prefix="/competitions", tags=["Social — Competencias"])
