
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse

from api.schemas.batch import BatchTaskResponse, BatchStatusResponse
from api.services.batch_service import BatchService

router = APIRouter(prefix="/batch", tags=["Batch Processing"])
batch_service = BatchService()

@router.post("/upload", response_model=BatchTaskResponse)
async def upload_batch_csv(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...)
):
    
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un .csv")

    task_id = str(uuid.uuid4())
    input_path = batch_service.INPUT_DIR / f"{task_id}_{file.filename}"

    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    background_tasks.add_task(batch_service.process_csv_task, task_id, input_path)

    return BatchTaskResponse(
        task_id=task_id,
        status="ACCEPTED",
        message="El archivo está siendo procesado en segundo plano."
    )

@router.get("/status/{task_id}", response_model=BatchStatusResponse)
def get_batch_status(task_id: str):
    status_info = batch_service.get_task_status(task_id)
    return BatchStatusResponse(
        task_id=task_id,
        status=status_info["status"],
        download_url=status_info["download_url"]
    )

@router.get("/download/{task_id}", response_class=FileResponse)
def download_batch_results(task_id: str):
    file_path = batch_service.get_output_file_path(task_id)
    return FileResponse(
        path=file_path,
        filename=f"predicciones_{task_id}.csv",
        media_type="text/csv"
    )