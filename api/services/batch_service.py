from pathlib import Path

import joblib
import pandas as pd
from fastapi import HTTPException


class BatchService:

    MODEL_PATH = "ml/saved_models/champion_model.joblib"
    INPUT_DIR = Path("data/batch_inputs")
    OUTPUT_DIR = Path("data/batch_outputs")

    def __init__(self):
        # Crear directorios si no existen
        self.INPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        try:
            self.model = joblib.load(self.MODEL_PATH)
        except Exception as e:
            raise RuntimeError(f"No se pudo cargar el modelo para Batch: {e}")

    def process_csv_task(self, task_id: str, file_path: Path) -> None:

        try:
            # 1. Leer CSV
            df = pd.read_csv(file_path)

            # 2. Validar que no tenga la variable objetivo si es un dataset nuevo
            if "Churn" in df.columns:
                X = df.drop(columns=["Churn"])
            else:
                X = df.copy()

            # 3. Predicción masiva (Vectorizada para máxima velocidad)
            probabilidades = self.model.predict_proba(X)[:, 1]
            predicciones = self.model.predict(X)

            # 4. Adjuntar resultados al DataFrame original
            df_result = df.copy()
            df_result["churn_risk_score"] = probabilidades
            df_result["will_churn"] = predicciones

            # 5. Guardar CSV de salida
            output_path = self.OUTPUT_DIR / f"{task_id}_output.csv"
            df_result.to_csv(output_path, index=False)

        except Exception as e:
            # En un entorno real, registraríamos este error con structlog o Sentry
            print(f"Error procesando la tarea {task_id}: {str(e)}")
            # Generar un archivo de error para informar al cliente
            error_path = self.OUTPUT_DIR / f"{task_id}_error.txt"
            error_path.write_text(f"Fallo en procesamiento: {str(e)}")

    def get_task_status(self, task_id: str) -> dict:
        output_path = self.OUTPUT_DIR / f"{task_id}_output.csv"
        error_path = self.OUTPUT_DIR / f"{task_id}_error.txt"

        if output_path.exists():
            return {"status": "COMPLETED", "download_url": f"/batch/download/{task_id}"}
        elif error_path.exists():
            return {"status": "FAILED", "download_url": None}
        else:
            return {"status": "PROCESSING", "download_url": None}

    def get_output_file_path(self, task_id: str) -> Path:
        output_path = self.OUTPUT_DIR / f"{task_id}_output.csv"
        if not output_path.exists():
            raise HTTPException(
                status_code=404, detail="Archivo no encontrado o tarea no completada"
            )
        return output_path
