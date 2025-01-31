from ydata.sdk.common.model import BaseModel
from ydata.sdk.common.types import UID as UID
from ydata.sdk.connectors._models.connector_type import ConnectorType

class Connector(BaseModel):
    uid: UID | None
    type: ConnectorType
    name: str | None
    def __eq__(self, other: object) -> bool: ...
