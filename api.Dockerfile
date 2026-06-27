# api.Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar algunas librerías de ML
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para aprovechar caché de capas de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código de la API, base de datos y modelos guardados
COPY api/ /app/api/
COPY database/ /app/database/
COPY ml/saved_models/ /app/ml/saved_models/
COPY ml/ /app/ml/

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]