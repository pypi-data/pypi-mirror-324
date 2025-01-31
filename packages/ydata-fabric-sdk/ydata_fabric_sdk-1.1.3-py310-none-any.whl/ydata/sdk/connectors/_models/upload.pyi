from ydata.sdk.common.model import BaseModel

class Upload(BaseModel):
    uid: str
    chunk_size: int
    file_name: str
    written_bytes: int | None
    total_bytes: int | None
