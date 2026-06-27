from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.schemas.churn import CustomerData, PredictionResponse
from api.services.prediction_service import PredictionService
from database.session import get_db

router = APIRouter(prefix="/predict", tags=["Predicción"])


@router.post("/", response_model=PredictionResponse)
def predict_churn(customer_data: CustomerData, db: Session = Depends(get_db)):

    service = PredictionService(db)
    return service.predict_single(customer_data)
