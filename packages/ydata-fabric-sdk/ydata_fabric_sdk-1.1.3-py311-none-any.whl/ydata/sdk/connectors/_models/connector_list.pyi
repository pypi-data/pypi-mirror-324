from dataclasses import dataclass
from typing import Any

class ConnectorsList(list):
    """Representation of the list of `Connectors` objects.

    The list inherits directly from Python `list`. The list does not
    communicate with the backend and thus, represent a snapshot at the
    moment it is created.
    """
    @dataclass(init=False)
    class ListItem:
        uid: str
        type: str
        name: str = ...
        creation_date: str = ...
        status: str = ...
        datasources_count: int | str = ...
    def get_by_name(self, name: str, default: Any | None = 'raise') -> dict | Any: ...
    def get_by_uid(self, uid: str, default: Any | None = 'raise') -> dict | Any: ...
