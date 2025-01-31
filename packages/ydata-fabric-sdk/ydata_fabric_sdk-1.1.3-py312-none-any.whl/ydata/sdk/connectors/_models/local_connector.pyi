from .connector import Connector

class LocalConnector(Connector):
    file: str | None
