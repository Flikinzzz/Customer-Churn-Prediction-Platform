#  Customer Churn Prediction Platform

Plataforma *Production-Ready* para la predicción de fuga de clientes (Churn), diseñada bajo principios de **Clean Architecture** y **DevOps**. Este proyecto demuestra un ciclo completo de vida de Machine Learning, desde la ingesta de datos hasta el despliegue de una API REST y un Dashboard interactivo.

##  Arquitectura del Sistema
El sistema utiliza una arquitectura desacoplada para garantizar escalabilidad y mantenibilidad.



##  Stack Tecnológico
- **Core:** Python 3.12, FastAPI, Pydantic v2
- **ML Engine:** Scikit-Learn, XGBoost, CatBoost, Optuna, SHAP, MLflow
- **Infraestructura:** Docker, Docker Compose, GitHub Actions
- **Dashboard:** Streamlit

##  Instalación & Ejecución Local
Asegúrate de tener Docker instalado y ejecutándose.

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/churn-platform.git](https://github.com/tu-usuario/churn-platform.git)
   cd churn-platform

2. ** Levantar servicios **
 docker compose up --build

3. ** Acceso en:  **

Dashboard: http://localhost:8501

API Docs (Swagger): http://localhost:8000/docs