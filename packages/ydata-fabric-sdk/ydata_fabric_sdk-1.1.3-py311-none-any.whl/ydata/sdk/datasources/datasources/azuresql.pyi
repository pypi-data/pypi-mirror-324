from ydata.sdk.common.client import Client as Client
from ydata.sdk.connectors.connector import Connector as Connector
from ydata.sdk.datasources._models.datatype import DataSourceType
from ydata.sdk.datasources.datasource import DataSource

class AzureSQLDataSource(DataSource):
    def __init__(self, connector: Connector, query: str, datatype: DataSourceType | str | None = ..., name: str | None = None, wait_for_metadata: bool = True, client: Client | None = None) -> None: ...
