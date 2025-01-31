from ydata.core.enum import StringEnum
from ydata.sdk.common.model import BaseModel
from ydata.sdk.common.status import GenericStateErrorStatus

class ValidationState(StringEnum):
    UNKNOWN: str
    VALIDATE: str
    VALIDATING: str
    FAILED: str
    AVAILABLE: str

class MetadataState(StringEnum):
    UNKNOWN: str
    GENERATE: str
    GENERATING: str
    FAILED: str
    AVAILABLE: str

class ProfilingState(StringEnum):
    UNKNOWN: str
    GENERATE: str
    GENERATING: str
    FAILED: str
    AVAILABLE: str

class State(StringEnum):
    """Represent the status of a [`DataSource`][ydata.sdk.datasources.datasource.DataSource]."""
    AVAILABLE: str
    PREPARING: str
    VALIDATING: str
    FAILED: str
    UNAVAILABLE: str
    DELETED: str
    UNKNOWN: str
ValidationStatus = GenericStateErrorStatus[ValidationState]
MetadataStatus = GenericStateErrorStatus[MetadataState]
ProfilingStatus = GenericStateErrorStatus[ProfilingState]

class Status(BaseModel):
    state: State | None
    validation: ValidationStatus | None
    metadata: MetadataStatus | None
    profiling: ProfilingStatus | None
    @staticmethod
    def unknown() -> Status: ...
