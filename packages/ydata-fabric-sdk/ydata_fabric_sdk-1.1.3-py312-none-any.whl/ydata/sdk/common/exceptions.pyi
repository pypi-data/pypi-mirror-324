from _typeshed import Incomplete
from pandas.errors import EmptyDataError as pdEmptyDataError
from ydata.core.error import FabricError

class SDKError(Exception):
    """Base Exception for all SDK errors."""
    def __init__(self, *args: object) -> None: ...

class ResponseError(FabricError):
    """Wrapper around Fabric Exception to capture error response from the
    backend."""
    description: Incomplete
    return_value: Incomplete
    def __init__(self, context: dict[str, str] | None = None, httpCode: int | None = None, name: str | None = None, description: str | None = None, returnValue: str | None = None) -> None: ...

class ClientException(SDKError):
    """Base Exception for Client related exceptions."""

class ClientCreationError(ClientException):
    """Raised when a Client could not be created."""
    def __init__(self, message: Incomplete | None = None) -> None: ...

class ClientHandshakeError(ClientException):
    """Raised when handshake could not be performed - likely a token issue"""
    auth_link: Incomplete
    def __init__(self, auth_link: str) -> None: ...

class ConnectorError(SDKError):
    """Base exception for ConnectorError."""
class InvalidConnectorError(ConnectorError):
    """Raised when a connector is invalid."""
class CredentialTypeError(ConnectorError):
    """Raised when credentials are not formed properly."""
class EmptyDataError(pdEmptyDataError, SDKError):
    """Raised when no data is available."""
class DataSourceError(SDKError):
    """Base exception for DataSourceError."""
class DataSourceNotAvailableError(DataSourceError):
    """Raised when a datasource needs to be available."""
class SynthesizerException(SDKError):
    """Base Exception for Synthesizer related exception."""
class NotReadyError(SynthesizerException):
    """Raised when a Synthesizer is not read."""
class NotTrainedError(SynthesizerException):
    """Raised when a Synthesizer is not trained."""

class NotInitializedError(SynthesizerException):
    """Raised when a Synthesizer is not initialized."""
    def __init__(self, message: str = 'The synthesizer is not initialized.\n Use `fit` to train the synthesizer or `get` to retrieve an existing instance.') -> None: ...

class AlreadyFittedError(SynthesizerException):
    """Raised when a Synthesizer is already trained."""
    def __init__(self, message: str = 'The synthesizer is already fitted!') -> None: ...

class DataTypeMissingError(SynthesizerException):
    """Raise when the DataType is missing and cannot be deduced from the
    context."""
class DataSourceAttrsError(SynthesizerException):
    """Raise when the DataSourceAttrs is missing or invalid."""
class FittingError(SynthesizerException):
    """Raised when a Synthesizer fails during training."""
class InputError(SDKError):
    """Raised for any user input related error."""
