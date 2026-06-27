from pydantic import BaseModel


class BatchTaskResponse(BaseModel):
    task_id: str
    status: str
    message: str


class BatchStatusResponse(BaseModel):
    task_id: str
    status: str
    download_url: str | None = None
