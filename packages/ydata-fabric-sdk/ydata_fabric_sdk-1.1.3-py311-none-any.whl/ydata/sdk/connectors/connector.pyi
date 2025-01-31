from pandas import DataFrame as pdDataFrame
from pathlib import Path
from ydata.sdk.common.client import Client as Client
from ydata.sdk.common.types import Project as Project, UID as UID
from ydata.sdk.connectors._models.connector_list import ConnectorsList
from ydata.sdk.connectors._models.connector_type import ConnectorType
from ydata.sdk.connectors._models.credentials.credentials import Credentials
from ydata.sdk.connectors._models.schema import Schema
from ydata.sdk.utils.model_mixin import ModelFactoryMixin

class Connector(ModelFactoryMixin):
    """A [`Connector`][ydata.sdk.connectors.Connector] allows to connect and
    access data stored in various places. The list of available connectors can
    be found [here][ydata.sdk.connectors.ConnectorType].

    Arguments:
        connector_type (Union[ConnectorType, str]): Type of the connector to be created
        credentials (dict): Connector credentials
        name (Optional[str]): (optional) Connector name
        project (Optional[Project]): (optional) Project name for this Connector
        client (Client): (optional) Client to connect to the backend

    Attributes:
        uid (UID): UID fo the connector instance (creating internally)
        type (ConnectorType): Type of the connector
    """
    def __init__(self, connector_type: ConnectorType | str | None = None, credentials: dict | None = None, name: str | None = None, project: Project | None = None, client: Client | None = None) -> None: ...
    @property
    def uid(self) -> UID: ...
    @property
    def name(self) -> str: ...
    @property
    def type(self) -> ConnectorType: ...
    @property
    def project(self) -> Project: ...
    @staticmethod
    def get(uid: UID, project: Project | None = None, client: Client | None = None) -> _T:
        """Get an existing connector.

        Arguments:
            uid (UID): Connector identifier
            project (Optional[Project]): (optional) Project name from where to get the connector
            client (Optional[Client]): (optional) Client to connect to the backend

        Returns:
            Connector
        """
    @staticmethod
    def create(connector_type: ConnectorType | str, credentials: str | Path | dict | Credentials, name: str | None = None, project: Project | None = None, client: Client | None = None) -> _T:
        """Create a new connector.

        Arguments:
            connector_type (Union[ConnectorType, str]): Type of the connector to be created
            credentials (dict): Connector credentials
            name (Optional[str]): (optional) Connector name
            project (Optional[Project]): (optional) Project where to create the connector
            client (Client): (optional) Client to connect to the backend

        Returns:
            New connector
        """
    @staticmethod
    def list(project: Project | None = None, client: Client | None = None) -> ConnectorsList:
        """List the connectors instances.

        Arguments:
            project (Optional[Project]): (optional) Project name from where to list the connectors
            client (Client): (optional) Client to connect to the backend

        Returns:
            List of connectors
        """

class RDBMSConnector(Connector):
    @property
    def schema(self) -> Schema | None: ...

class LocalConnector(Connector):
    @staticmethod
    def create(source: pdDataFrame | str | Path, connector_type: ConnectorType | str = ..., name: str | None = None, project: Project | None = None, client: Client | None = None) -> LocalConnector:
        """Create a new connector.

        Arguments:
            source (Union[pdDataFrame, str, Path]): pandas dataframe, string or path to a file
            name (Optional[str]): (optional) Connector name
            project (Optional[Project]): (optional) Project where to create the connector
            client (Client): (optional) Client to connect to the backend

        Returns:
            New connector
        """
