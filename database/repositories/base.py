"""Interfaz abstracta para el patrón repositorio."""

from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """Clase base abstracta que define las operaciones CRUD estándar."""

    def __init__(self, model: type[ModelType], db: Session) -> None:
        """Inicializa el repositorio con un modelo específico y la sesión.

        Args:
            model: Clase del modelo de SQLAlchemy.
            db: Sesión activa de la base de datos.
        """
        self.model = model
        self.db = db

    def get(self, id: Any) -> ModelType | None:
        """Busca un registro por su clave primaria."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """Retorna una lista paginada de registros."""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: ModelType) -> ModelType:
        """Persiste un nuevo registro en la base de datos."""
        self.db.add(obj_in)
        self.db.commit()
        self.db.refresh(obj_in)
        return obj_in
