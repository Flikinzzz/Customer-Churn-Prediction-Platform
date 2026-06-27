import pandas as pd

from ml.pipeline.preprocessor import create_preprocessor_pipeline
from scripts.download_data import download_dataset

# 1. Descargar datos
download_dataset()

# 2. Cargar datos
print("Cargando CSV...")
df = pd.read_csv("data/raw/telco_churn.csv")
print(f"Forma original: {df.shape}")

# Separar variables predictoras (X) del target (y)
X = df.drop(columns=["Churn"])

# 3. Crear y ajustar el Pipeline
print("Inicializando Pipeline...")
pipeline = create_preprocessor_pipeline()

print("Ajustando (Fit) y Transformando (Transform) los datos...")
X_processed = pipeline.fit_transform(X)

# 4. Validar salida
# Scikit-learn nos devuelve los nombres de las columnas generadas (OneHot)
feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()

print(f"Forma después del preprocesamiento: {X_processed.shape}")
print(f"Ejemplo de nuevas variables: {feature_names[-5:]}")
print("El pipeline está 100% operativo y listo para modelos.")
