from _typeshed import Incomplete
from httpx import Response as Response, codes as http_codes
from httpx._types import RequestContent as RequestContent
from ydata.sdk.common.client.singleton import SingletonClient
from ydata.sdk.common.types import Project

codes = http_codes
HELP_TEXT: Incomplete

class Client(metaclass=SingletonClient):
    """Main Client class used to abstract the connection to the backend.

    A normal user should not have to instanciate a [`Client`][ydata.sdk.common.client.Client] by itself.
    However, in the future it will be useful for power-users to manage projects and connections.

    Args:
        credentials (Optional[dict]): (optional) Credentials to connect
        project (Optional[Project]): (optional) Project to connect to. If not specified, the client will connect to the default user's project.
    """
    codes = codes
    DEFAULT_PROJECT: Project | None
    def __init__(self, credentials: str | dict | None = None, project: Project | None = None, set_as_global: bool = False) -> None: ...
    @property
    def project(self) -> Project: ...
    @project.setter
    def project(self, value: Project): ...
    def post(self, endpoint: str, content: RequestContent | None = None, data: dict | None = None, json: dict | None = None, project: Project | None = None, files: dict | None = None, raise_for_status: bool = True) -> Response:
        """POST request to the backend.

        Args:
            endpoint (str): POST endpoint
            content (Optional[RequestContent])
            data (Optional[dict]): (optional) multipart form data
            json (Optional[dict]): (optional) json data
            files (Optional[dict]): (optional) files to be sent
            raise_for_status (bool): raise an exception on error

        Returns:
            Response object
        """
    def patch(self, endpoint: str, content: RequestContent | None = None, data: dict | None = None, json: dict | None = None, project: Project | None = None, files: dict | None = None, raise_for_status: bool = True) -> Response:
        """PATCH request to the backend.

        Args:
            endpoint (str): POST endpoint
            content (Optional[RequestContent])
            data (Optional[dict]): (optional) multipart form data
            json (Optional[dict]): (optional) json data
            files (Optional[dict]): (optional) files to be sent
            raise_for_status (bool): raise an exception on error

        Returns:
            Response object
        """
    def get(self, endpoint: str, params: dict | None = None, project: Project | None = None, cookies: dict | None = None, raise_for_status: bool = True) -> Response:
        """GET request to the backend.

        Args:
            endpoint (str): GET endpoint
            cookies (Optional[dict]): (optional) cookies data
            raise_for_status (bool): raise an exception on error

        Returns:
            Response object
        """
    def get_static_file(self, endpoint: str, project: Project | None = None, raise_for_status: bool = True) -> Response:
        """Retrieve a static file from the backend.

        Args:
            endpoint (str): GET endpoint
            raise_for_status (bool): raise an exception on error

        Returns:
            Response object
        """
