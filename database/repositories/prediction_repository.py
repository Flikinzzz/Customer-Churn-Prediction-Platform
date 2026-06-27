"""Implementación del repositorio para el modelo de predicciones."""

from collections.abc import Sequence
from sqlalchemy.orm import Session
from database.models.prediction import PredictionModel
from database.repositories.base import BaseRepository


class PredictionRepository(BaseRepository[PredictionModel]):
    """Repositorio especializado en la gestión de predicciones e historial."""

    def __init__(self, db: Session) -> None:
        super().__init__(PredictionModel, db)

    def get_by_customer_id(self, customer_id: str) -> Sequence[PredictionModel]:
        """Obtiene todo el historial de predicciones asociado a un cliente.

        Args:
            customer_id: Identificador único del cliente.

        Returns:
            Sequence[PredictionModel]: Lista de predicciones ordenadas por fecha.
        """
        return (
            self.db.query(self.model)
            .filter(self.model.customer_id == customer_id)
            .order_index(self.model.created_at.desc())
            .all()
        )

    def update_ground_truth(self, prediction_id: int, actual_label: int) -> PredictionModel | None:
        """Actualiza el resultado real (ground truth) para evaluar la precisión del modelo.

        Args:
            prediction_id: ID de la predicción registrada.
            actual_label: 1 si el cliente efectivamente se fugó, 0 si no.

        Returns:
            PredictionModel | None: El modelo actualizado o None si no existe.
        """
        prediction = self.get(prediction_id)
        if prediction:
            prediction.actual_label = actual_label
            self.db.commit()
            self.db.refresh(prediction)
        return prediction