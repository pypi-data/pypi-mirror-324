from ydata.sdk.common.client import Client as Client
from ydata.sdk.common.types import Project as Project
from ydata.sdk.connectors.connector import LocalConnector as LocalConnector
from ydata.sdk.datasources._models.datatype import DataSourceType
from ydata.sdk.datasources._models.filetype import FileType
from ydata.sdk.datasources.datasource import DataSource

class LocalDataSource(DataSource):
    def __init__(self, connector: LocalConnector, name: str | None = None, project: Project | None = None, datatype: DataSourceType | str | None = ..., filetype: FileType | str = ..., separator: str = ',', wait_for_metadata: bool = True, client: Client | None = None) -> None: ...
