from ydata.sdk.common.model import BaseModel
from ydata.sdk.common.pydantic_utils import to_camel

class BaseConfig(BaseModel.Config):
    alias_generator = to_camel

class TableColumn(BaseModel):
    """Class to store the information of a Column table."""
    name: str
    variable_type: str
    primary_key: bool | None
    is_foreign_key: bool | None
    foreign_keys: list
    nullable: bool
    Config = BaseConfig

class Table(BaseModel):
    """Class to store the table columns information."""
    name: str
    columns: list[TableColumn]
    primary_keys: list[TableColumn]
    foreign_keys: list[TableColumn]
    Config = BaseConfig

class Schema(BaseModel):
    """Class to store the database schema information."""
    name: str
    tables: list[Table] | None
    Config = BaseConfig
