from ydata.sdk.common.types import UID as UID
from ydata.sdk.datasources._models.datatype import DataSourceType
from ydata.sdk.datasources._models.metadata.metadata import Metadata
from ydata.sdk.datasources._models.status import Status

class DataSource:
    uid: UID | None
    author: str | None
    name: str | None
    datatype: DataSourceType | None
    metadata: Metadata | None
    status: Status | None
    connector_ref: str | None
    connector_type: str | None
    def __post_init__(self) -> None: ...
    def to_payload(self): ...
