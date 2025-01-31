from _typeshed import Incomplete
from pathlib import Path
from ydata.sdk.common.client.client import Client

CLIENT_INIT_TIMEOUT: Incomplete
WAITING_FOR_CLIENT: bool

def get_client(client_or_creds: Client | dict | str | Path | None = None, set_as_global: bool = False, wait_for_auth: bool = True) -> Client:
    """Deduce how to initialize or retrieve the client.

    This is meant to be a zero configuration for the user.

    Example: Create and set a client globally
            ```py
            from ydata.sdk.client import get_client
            get_client(set_as_global=True)
            ```

    Args:
        client_or_creds (Optional[Union[Client, dict, str, Path]]): Client to forward or credentials for initialization
        set_as_global (bool): If `True`, set client as global
        wait_for_auth (bool): If `True`, wait for the user to authenticate

    Returns:
        Client instance
    """
def init_client(func):
    """Decorator to intialize a client automatically.

    It intercept a client object in the decorated functionc all and wrap
    it with `get_client` function.
    """
