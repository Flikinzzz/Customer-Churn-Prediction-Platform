"""Transformadores personalizados para Feature Engineering compatibles con Scikit-Learn."""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class TelcoDataCleaner(BaseEstimator, TransformerMixin):
    """Limpia inconsistencias nativas del dataset Telco Churn."""

    def fit(self, X: pd.DataFrame, y: pd.Series | None = None) -> "TelcoDataCleaner":
        """Método fit (no hace nada, requerido por la interfaz)."""
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transforma el dataframe limpiando valores nulos ocultos.

        Args:
            X: DataFrame de entrada.

        Returns:
            DataFrame con la limpieza aplicada.
        """
        X_clean = X.copy()
        
        # El dataset tiene espacios en blanco " " en TotalCharges cuando tenure es 0
        if "TotalCharges" in X_clean.columns:
            X_clean["TotalCharges"] = (
                X_clean["TotalCharges"]
                .replace(r"^\s*$", "0.0", regex=True)
                .astype(float)
            )
            
        # Eliminar el ID del cliente ya que no tiene valor predictivo
        if "customerID" in X_clean.columns:
            X_clean = X_clean.drop(columns=["customerID"])
            
        return X_clean


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """Genera variables derivadas (Feature Engineering) para mejorar el modelo."""

    def fit(self, X: pd.DataFrame, y: pd.Series | None = None) -> "FeatureEngineer":
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Aplica la creación de nuevas características.

        Args:
            X: DataFrame preprocesado.

        Returns:
            DataFrame con nuevas columnas.
        """
        X_eng = X.copy()
        
        # 1. Agrupar 'tenure' (antigüedad) en bins lógicos (años)
        if "tenure" in X_eng.columns:
            X_eng["TenureGroup"] = pd.cut(
                X_eng["tenure"],
                bins=[-1, 12, 24, 36, 48, 60, 100],
                labels=["0-1 Year", "1-2 Years", "2-3 Years", "3-4 Years", "4-5 Years", "5+ Years"],
            ).astype(str)

        # 2. Ratio de cargos (Cargos totales vs Cargos mensuales)
        # Esto ayuda al modelo a identificar inconsistencias en facturación
        if "TotalCharges" in X_eng.columns and "MonthlyCharges" in X_eng.columns:
            X_eng["ChargeRatio"] = X_eng["TotalCharges"] / (X_eng["MonthlyCharges"] + 1e-5)

        return X_eng