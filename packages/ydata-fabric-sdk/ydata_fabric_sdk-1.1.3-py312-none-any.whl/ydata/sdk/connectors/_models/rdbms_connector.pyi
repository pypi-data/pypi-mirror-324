from .connector import Connector
from ydata.sdk.connectors._models.schema import Schema

class RDBMSConnector(Connector):
    db_schema: Schema | None
