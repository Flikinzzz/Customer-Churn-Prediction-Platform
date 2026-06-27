"""Módulo de Explainable AI utilizando SHAP."""

import os
import shap
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline

class ShapExplainer:
    """Genera explicaciones de los modelos usando valores SHAP."""

    def __init__(self, pipeline: Pipeline, output_dir: str = "docs/assets/images"):
        self.pipeline = pipeline
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Extraer los componentes del pipeline
        self.preprocessor = self.pipeline.named_steps['preprocessor']
        self.model = self.pipeline.named_steps['classifier']

    def generate_global_explanations(self, X_sample: pd.DataFrame) -> None:
        """Genera gráficos de importancia global (Summary Plot)."""
        # Transformar los datos crudos a través del preprocesador
        X_transformed = self.preprocessor.transform(X_sample)
        
        # Obtener los nombres de las features después del OneHotEncoding
        feature_names = self.preprocessor[-1].get_feature_names_out()
        X_transformed_df = pd.DataFrame(X_transformed, columns=feature_names)

        # Crear el explainer. Dependiendo del tipo de modelo, usamos Tree o Linear
        try:
            # TreeExplainer es mucho más rápido para XGBoost/LightGBM/CatBoost/RF
            explainer = shap.TreeExplainer(self.model)
            shap_values = explainer.shap_values(X_transformed_df)
        except Exception:
            # Fallback para Regresión Logística u otros modelos
            explainer = shap.Explainer(self.model, X_transformed_df)
            shap_values = explainer(X_transformed_df).values

        # Asegurarnos de usar la clase positiva (Churn=1) si devuelve una lista (ej. RandomForest)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        # 1. Summary Plot (Beeswarm)
        plt.figure()
        shap.summary_plot(shap_values, X_transformed_df, show=False)
        plt.title("SHAP Summary Plot")
        plt.savefig(f"{self.output_dir}/shap_summary.png", bbox_inches='tight')
        plt.close()
        
        # 2. Feature Importance Bar Plot
        plt.figure()
        shap.summary_plot(shap_values, X_transformed_df, plot_type="bar", show=False)
        plt.title("SHAP Feature Importance")
        plt.savefig(f"{self.output_dir}/shap_bar.png", bbox_inches='tight')
        plt.close()