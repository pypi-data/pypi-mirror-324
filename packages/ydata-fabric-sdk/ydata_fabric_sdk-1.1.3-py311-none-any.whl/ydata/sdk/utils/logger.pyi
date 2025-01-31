import logging

def is_running_in_databricks(): ...
def get_datasource_info(dataframe, datatype):
    """
        calculate required datasource info
    """
def analytics_features(datatype: str, connector: str, nrows: int, ncols: int, ntables: int, method: str, dbx: str) -> None:
    """
        Returns metrics and analytics from ydata-fabric-sdk
    """

class SDKLogger(logging.Logger):
    def __init__(self, name: str, level: int = ...) -> None: ...
    def info(self, dataframe, datatype: str, method: str) -> None: ...
