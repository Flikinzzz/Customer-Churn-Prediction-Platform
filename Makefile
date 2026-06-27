.PHONY: help install format lint test run-api run-ui

help:
	@echo "Comandos disponibles:"
	@echo "  install    Instala las dependencias (requiere entorno virtual)"
	@echo "  format     Formatea el código con Black e isort"
	@echo "  lint       Revisa el código con Ruff"
	@echo "  test       Ejecuta las pruebas con Pytest"
	@echo "  run-api    Inicia el servidor FastAPI"
	@echo "  run-ui     Inicia el dashboard de Streamlit"

install:
	pip install --upgrade pip
	pip install -r requirements.txt
evaluate:
	python -m scripts.evaluate_model
	
format:
	black .
	isort .

lint:
	ruff check .

test:
	pytest

run-api:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

run-ui:
	streamlit run ui/app.py