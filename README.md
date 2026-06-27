# Customer Churn Prediction Platform

Una plataforma empresarial e integral de extremo a extremo (End-to-End) diseñada para predecir la fuga de clientes (*Customer Churn*). Este sistema combina ingeniería de software de alto nivel mediante **Clean Architecture** con un pipeline moderno de **MLOps**, exponiendo un motor predictivo altamente escalable y automatizado.

La plataforma permite tanto la inferencia en tiempo real como el procesamiento asíncrono por lotes (*Batch Processing*), transformando métricas complejas de Machine Learning en herramientas de toma de decisiones visuales y accesibles para usuarios de negocio.

## Enlaces del Proyecto (Live Demo)
* **Dashboard  (UI):** [https://customer-churn-prediction-platform-5k5a3mc69taczdd2pxvzkr.streamlit.app/]
* **Documentación de la API (Swagger):** [https://churn-api-production-w9fi.onrender.com/docs]
WIP
* **Pipeline de CI/CD:** [![CI/CD Workflow](https://github.com/[Tu-Usuario]/[Tu-Repo]/actions/workflows/ci.yml/badge.svg)](https://github.com/[Tu-Usuario]/[Tu-Repo]/actions)

---

## Estructura del Proyecto

El repositorio está organizado siguiendo los principios de Clean Architecture, separando claramente el motor de Machine Learning, la API de backend y la interfaz gráfica.

.
├── api.Dockerfile          # Construcción del contenedor Docker para la API (Backend)
├── ui.Dockerfile           # Construcción del contenedor Docker para Streamlit (Frontend)
├── docker-compose.yml      # Orquestación para levantar ambos servicios localmente
├── Makefile                # Atajos de comandos para pruebas, linting y ejecución
├── pyproject.toml          # Configuración de herramientas (Ruff, Black, Pytest)
├── requirements.txt        # Dependencias de Python consolidadas
│
├── api/                    # Capa de Presentación (REST API)
│   ├── main.py             # Punto de entrada de FastAPI y configuración de la app
│   ├── routes/             # Endpoints expuestos (predict.py, batch.py, health.py)
│   ├── schemas/            # Contratos de datos y validaciones estrictas de negocio (Pydantic)
│   └── services/           # Lógica de orquestación e inyección de dependencias (Lazy Loading)
│
├── database/               # Capa de Persistencia (Almacenamiento de auditoría)
│   ├── base.py             # Configuración declarativa de SQLAlchemy
│   ├── session.py          # Manejo de conexiones a la base de datos
│   ├── models/             # Esquemas de tablas (almacenamiento de predicciones históricas)
│   └── repositories/       # Abstracción de consultas CRUD (Patrón Repository)
│
├── ml/                     # Motor de Machine Learning (Core Científico)
│   ├── inference/          # Scripts para predicción en vivo y generador de explicabilidad (SHAP)
│   ├── pipeline/           # Feature Engineering y transformadores personalizados (Scikit-Learn)
│   ├── training/           # Optimización de hiperparámetros (Optuna) y entrenamiento
│   └── saved_models/       # Directorio de artefactos (contiene el champion_model.joblib)
│
├── scripts/                # Tareas operativas y automatización MLOps
│   ├── download_data.py    # Descarga automatizada del dataset inicial
│   ├── evaluate_model.py   # Generador de métricas y gráficos (ROC, Matriz de Confusión)
│   └── train_run.py        # Pipeline de ejecución de entrenamiento y registro
│
├── tests/                  # Pruebas automatizadas (CI/CD)
│   └── test_api.py         # Tests unitarios y de integración usando TestClient
│
└── ui/                     # Interfaz Gráfica Accesible
    └── app.py              # Dashboard interactivo en Streamlit que consume la API REST