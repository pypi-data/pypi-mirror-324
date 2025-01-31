from ydata.sdk.common.client import Client as Client
from ydata.sdk.common.types import Project as Project, UID as UID
from ydata.sdk.connectors.connector import Connector
from ydata.sdk.datasources._models.datatype import DataSourceType
from ydata.sdk.datasources._models.metadata.data_types import DataType as DataType
from ydata.sdk.synthesizers.synthesizer import BaseSynthesizer

class MultiTableSynthesizer(BaseSynthesizer):
    """MultiTable synthesizer class.

    Methods
    -------
    - `fit`: train a synthesizer instance.
    - `sample`: request synthetic data.
    - `status`: current status of the synthesizer instance.

    Note:
            The synthesizer instance is created in the backend only when the `fit` method is called.

    Arguments:
        write_connector (UID | Connector): Connector of type RDBMS to be used to write the samples
        uid (UID): (optional) UID to identify this synthesizer
        name (str): (optional) Name to be used when creating the synthesizer. Calculated internally if not provided
        client (Client): (optional) Client to connect to the backend
    """
    def __init__(self, write_connector: Connector | UID, uid: UID | None = None, name: str | None = None, project: Project | None = None, client: Client | None = None) -> None: ...
    def fit(self, X, datatype: DataSourceType | str | None = None, dtypes: dict[str, str | DataType] | None = None, anonymize: dict | None = None) -> None:
        """Fit the synthesizer.

        The synthesizer accepts as training dataset a YData [`DataSource`][ydata.sdk.datasources.DataSource].
        Except X, all the other arguments are for now ignored until they are supported.

        Arguments:
            X (DataSource): DataSource to Train
        """
    def sample(self, frac: int | float = 1, write_connector: Connector | UID | None = None) -> None:
        """Sample from a [`MultiTableSynthesizer`][ydata.sdk.synthesizers.MultiTableSynthesizer]
        instance.
        The sample is saved in the connector that was provided in the synthesizer initialization
        or in the

        Arguments:
            frac (int | float): fraction of the sample to be returned
        """
