import urllib.request
from pathlib import Path

DATASET_URL = (
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/"
    "master/data/Telco-Customer-Churn.csv"
)


def download_dataset() -> None:
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "data" / "raw"

    raw_dir.mkdir(parents=True, exist_ok=True)

    file_path = raw_dir / "telco_churn.csv"

    if file_path.exists():
        print(f"✅ El dataset ya existe en: {file_path}")
        return

    print(f"⏳ Descargando dataset desde {DATASET_URL}...")
    try:
        urllib.request.urlretrieve(DATASET_URL, file_path)
        print(f"Dataset descargado exitosamente en: {file_path}")
    except Exception as e:
        print(f"Error al descargar el dataset: {e}")


if __name__ == "__main__":
    download_dataset()
