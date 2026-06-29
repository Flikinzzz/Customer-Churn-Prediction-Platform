import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from ml.inference.evaluator import ModelEvaluator
from ml.inference.explainer import ShapExplainer


def main():
    print("Cargando dataset y modelo campeón...")
    df = pd.read_csv("data/raw/telco_churn.csv")
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = joblib.load("ml/saved_models/champion_model.joblib")

    y_prob = pipeline.predict_proba(X_test)[:, 1]
    y_pred = pipeline.predict(X_test)

    print("Calculando métricas y gráficas...")
    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate(y_test, y_prob, y_pred)

    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

    evaluator.plot_roc_curve(y_test, y_prob)
    evaluator.plot_confusion_matrix(y_test, y_pred)
    evaluator.plot_calibration_curve(y_test, y_prob)

    print("Generando explicaciones SHAP (esto puede tardar unos segundos)...")
    explainer = ShapExplainer(pipeline)

    X_sample = X_test.sample(200, random_state=42)
    explainer.generate_global_explanations(X_sample)

    print("✅ Todas las métricas e imágenes generadas en 'docs/assets/images/'")


if __name__ == "__main__":
    main()
