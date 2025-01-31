from ydata.core.enum import StringEnum

class Level(StringEnum):
    """Warning levels."""
    MODERATE: int
    HIGH: int

class WarningType(StringEnum):
    """Warning types."""
    SKEWNESS: str
    MISSINGS: str
    CARDINALITY: str
    DUPLICATES: str
    IMBALANCE: str
    CONSTANT: str
    INFINITY: str
    ZEROS: str
    CORRELATION: str
    UNIQUE: str
    UNIFORM: str
    CONSTANT_LENGTH: str
