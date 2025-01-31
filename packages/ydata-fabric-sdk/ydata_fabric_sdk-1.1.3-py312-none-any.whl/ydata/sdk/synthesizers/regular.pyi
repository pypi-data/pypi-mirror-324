from pandas import DataFrame as pdDataFrame
from ydata.datascience.common import PrivacyLevel
from ydata.sdk.datasources._models.metadata.data_types import DataType as DataType
from ydata.sdk.synthesizers.synthesizer import BaseSynthesizer

class RegularSynthesizer(BaseSynthesizer):
    def sample(self, n_samples: int = 1, condition_on: dict | None = None) -> pdDataFrame:
        """Sample from a [`RegularSynthesizer`][ydata.sdk.synthesizers.RegularSynthesizer]
        instance.

        Arguments:
            n_samples (int): number of rows in the sample
            condition_on: (Optional[dict]): (optional) conditional sampling parameters

        Returns:
            synthetic data
        """
    def fit(self, X, privacy_level: PrivacyLevel = ..., entities: str | list[str] | None = None, generate_cols: list[str] | None = None, exclude_cols: list[str] | None = None, dtypes: dict[str, str | DataType] | None = None, target: str | None = None, anonymize: dict | None = None, condition_on: list[str] | None = None) -> None:
        """Fit the synthesizer.

        The synthesizer accepts as training dataset either a pandas [`DataFrame`][pandas.DataFrame] directly or a YData [`DataSource`][ydata.sdk.datasources.DataSource].

        Arguments:
            X (Union[DataSource, pandas.DataFrame]): Training dataset
            privacy_level (PrivacyLevel): Synthesizer privacy level (defaults to high fidelity)
            entities (Union[str, List[str]]): (optional) columns representing entities ID
            generate_cols (List[str]): (optional) columns that should be synthesized
            exclude_cols (List[str]): (optional) columns that should not be synthesized
            dtypes (Dict[str, Union[str, DataType]]): (optional) datatype mapping that will overwrite the datasource metadata column datatypes
            target (Optional[str]): (optional) Target column
            name (Optional[str]): (optional) Synthesizer instance name
            anonymize (Optional[str]): (optional) fields to anonymize and the anonymization strategy
            condition_on: (Optional[List[str]]): (optional) list of features to condition upon
        """
