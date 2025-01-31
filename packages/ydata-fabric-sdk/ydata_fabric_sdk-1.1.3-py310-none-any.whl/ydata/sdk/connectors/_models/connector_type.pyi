from enum import Enum

class ConnectorType(str, Enum):
    AWS_S3 = 'aws-s3'
    AZURE_BLOB = 'azure-blob'
    GCS = 'gcs'
    FILE = 'file'
    MYSQL = 'mysql'
    AZURE_SQL = 'azure-sql'
    BIGQUERY = 'google-bigquery'
    SNOWFLAKE = 'snowflake'
    @property
    def is_rdbms(self) -> bool: ...
