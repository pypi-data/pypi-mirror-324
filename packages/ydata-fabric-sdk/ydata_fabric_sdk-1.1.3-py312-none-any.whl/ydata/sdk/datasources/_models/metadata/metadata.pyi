from ydata.sdk.common.model import BaseModel
from ydata.sdk.datasources._models.metadata.column import Column
from ydata.sdk.datasources._models.metadata.warnings import MetadataWarning

class Cardinality(BaseModel):
    column: str
    value: int

class LongTextStatistics(BaseModel):
    average_number_of_characters: int
    average_number_of_words: int

class Metadata(BaseModel):
    """The Metadata object contains descriptive information about a.

    [`DataSource`](ydata.sdk.datasources.datasource)

    Attributes:
        columns (List[Column]): columns information
    """
    cardinality: list[Cardinality] | None
    columns: list[Column]
    duplicate_rows: int
    long_text_statistics: LongTextStatistics | None
    memory: str
    missing_cells: int
    number_of_rows: int
    warnings: list[MetadataWarning] | None
