
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve, confusion_matrix
)
import numpy as np
from sklearn.calibration import calibration_curve

class ModelEvaluator:

    def __init__(self, output_dir: str = "docs/assets/images"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        # Configuración estética global
        sns.set_theme(style="whitegrid")

    def evaluate(self, y_true: np.ndarray, y_prob: np.ndarray, y_pred: np.ndarray) -> dict:
        return {
            "Accuracy": accuracy_score(y_true, y_pred),
            "Precision": precision_score(y_true, y_pred),
            "Recall": recall_score(y_true, y_pred),
            "F1_Score": f1_score(y_true, y_pred),
            "ROC_AUC": roc_auc_score(y_true, y_prob)
        }

    def plot_roc_curve(self, y_true: np.ndarray, y_prob: np.ndarray) -> None:
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        auc = roc_auc_score(y_true, y_prob)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {auc:.3f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC)')
        plt.legend(loc="lower right")
        plt.savefig(f"{self.output_dir}/roc_curve.png", bbox_inches='tight')
        plt.close()

    def plot_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.title('Confusion Matrix')
        plt.savefig(f"{self.output_dir}/confusion_matrix.png", bbox_inches='tight')
        plt.close()

    def plot_calibration_curve(self, y_true: np.ndarray, y_prob: np.ndarray) -> None:
        prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10)
        
        plt.figure(figsize=(8, 6))
        plt.plot(prob_pred, prob_true, marker='o', linewidth=1, label='Model')
        plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfectly calibrated')
        plt.xlabel('Mean predicted probability')
        plt.ylabel('Fraction of positives')
        plt.title('Calibration Curve')
        plt.legend()
        plt.savefig(f"{self.output_dir}/calibration_curve.png", bbox_inches='tight')
        plt.close()