"""Orquestador del pipeline de preprocesamiento de Machine Learning."""

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from ml.pipeline.features import FeatureEngineer, TelcoDataCleaner


def create_preprocessor_pipeline() -> Pipeline:
    """Construye el pipeline completo de preprocesamiento.

    Returns:
        Pipeline: Un objeto Scikit-Learn Pipeline listo para hacer fit/transform.
    """
    # Variables después del feature engineering que necesitamos separar
    numeric_features = ["tenure", "MonthlyCharges", "TotalCharges", "ChargeRatio"]
    
    categorical_features = [
        "gender", "SeniorCitizen", "Partner", "Dependents", 
        "PhoneService", "MultipleLines", "InternetService", 
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", 
        "TechSupport", "StreamingTV", "StreamingMovies", 
        "Contract", "PaperlessBilling", "PaymentMethod", "TenureGroup"
    ]

    # Transformaciones por tipo de dato
    numeric_transformer = Pipeline(steps=[
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    # Ensamblar ColumnTransformer
    column_processor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    # Pipeline maestro
    full_pipeline = Pipeline(steps=[
        ("cleaner", TelcoDataCleaner()),
        ("engineer", FeatureEngineer()),
        ("preprocessor", column_processor)
    ])

    return full_pipeline