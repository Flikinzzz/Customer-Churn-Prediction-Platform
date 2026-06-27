
from fastapi import APIRouter
from datetime import datetime, UTC

router = APIRouter(tags=["Operaciones"])

@router.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now(UTC).isoformat()}

@router.get("/version")
def get_version():
    return {"api_version": "1.0.0", "model_version": "v1.0.0"}