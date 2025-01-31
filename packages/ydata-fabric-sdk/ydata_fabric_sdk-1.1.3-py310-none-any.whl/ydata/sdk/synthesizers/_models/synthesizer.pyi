from .status import Status
from ydata.sdk.common.model import BaseModel

class Synthesizer(BaseModel):
    uid: str | None
    author: str | None
    name: str | None
    status: Status | None
