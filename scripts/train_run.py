"""Script ejecutable para lanzar el entrenamiento completo."""

import pandas as pd

from ml.training.trainer import ModelTrainer


def main():
    print("Cargando dataset...")
    df = pd.read_csv("data/raw/telco_churn.csv")

    # Preparar target (convertir 'Yes'/'No' a 1/0)
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    trainer = ModelTrainer()
    trainer.run_training_pipeline(X, y)


if __name__ == "__main__":
    main()
