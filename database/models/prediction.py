
from datetime import datetime, UTC
from typing import Any
from sqlalchemy import JSON, Float, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class PredictionModel(Base):

    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    
    # Almacenamos el payload completo de entrada como JSON para flexibilidad ante cambios de schema
    features: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    
    # Resultados del modelo
    prediction_score: Mapped[float] = mapped_column(Float, nullable=False)
    prediction_label: Mapped[int] = mapped_column(Integer, nullable=False)
    model_version: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    
    # Retroalimentación o etiqueta real para cálculo de Drift y reentrenamiento (Ground Truth)
    actual_label: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )