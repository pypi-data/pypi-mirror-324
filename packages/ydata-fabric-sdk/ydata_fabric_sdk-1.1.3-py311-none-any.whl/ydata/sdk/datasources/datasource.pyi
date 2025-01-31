from ydata.sdk.common.client import Client as Client
from ydata.sdk.common.types import Project as Project, UID as UID
from ydata.sdk.connectors.connector import Connector as Connector
from ydata.sdk.datasources._models.datasource_list import DataSourceList
from ydata.sdk.datasources._models.datatype import DataSourceType
from ydata.sdk.datasources._models.metadata.metadata import Metadata
from ydata.sdk.datasources._models.status import Status
from ydata.sdk.utils.model_mixin import ModelFactoryMixin

class DataSource(ModelFactoryMixin):
    """A [`DataSource`][ydata.sdk.datasources.DataSource] represents a dataset
    to be used by a Synthesizer as training data.

    Arguments:
        connector (Connector): Connector from which the datasource is created
        datatype (Optional[Union[DataSourceType, str]]): (optional) DataSource type
        name (Optional[str]): (optional) DataSource name
        project (Optional[Project]): (optional) Project name for this datasource
        wait_for_metadata (bool): If `True`, wait until the metadata is fully calculated
        client (Client): (optional) Client to connect to the backend
        **config: Datasource specific configuration

    Attributes:
        uid (UID): UID fo the datasource instance
        datatype (DataSourceType): Data source type
        status (Status): Status of the datasource
        metadata (Metadata): Metadata associated to the datasource
    """
    def __init__(self, connector: Connector, datatype: DataSourceType | str | None = ..., name: str | None = None, project: Project | None = None, wait_for_metadata: bool = True, client: Client | None = None, **config) -> None: ...
    @property
    def uid(self) -> UID: ...
    @property
    def datatype(self) -> DataSourceType: ...
    @property
    def project(self) -> Project: ...
    @property
    def status(self) -> Status: ...
    @property
    def metadata(self) -> Metadata | None: ...
    @staticmethod
    def list(project: Project | None = None, client: Client | None = None) -> DataSourceList:
        """List the  [`DataSource`][ydata.sdk.datasources.DataSource]
        instances.

        Arguments:
            project (Optional[Project]): (optional) Project name from where to list the datasources
            client (Client): (optional) Client to connect to the backend

        Returns:
            List of datasources
        """
    @staticmethod
    def get(uid: UID, project: Project | None = None, client: Client | None = None) -> DataSource:
        """Get an existing [`DataSource`][ydata.sdk.datasources.DataSource].

        Arguments:
            uid (UID): DataSource identifier
            project (Optional[Project]): (optional) Project name from where to get the connector
            client (Client): (optional) Client to connect to the backend

        Returns:
            DataSource
        """
    @classmethod
    def create(cls, connector: Connector, datatype: DataSourceType | str | None = ..., name: str | None = None, project: Project | None = None, wait_for_metadata: bool = True, client: Client | None = None, **config) -> DataSource:
        """Create a new [`DataSource`][ydata.sdk.datasources.DataSource].

        Arguments:
            connector (Connector): Connector from which the datasource is created
            datatype (Optional[Union[DataSourceType, str]]): (optional) DataSource type
            name (Optional[str]): (optional) DataSource name
            project (Optional[Project]): (optional) Project name for this datasource
            wait_for_metadata (bool): If `True`, wait until the metadata is fully calculated
            client (Client): (optional) Client to connect to the backend
            **config: Datasource specific configuration

        Returns:
            DataSource
        """
