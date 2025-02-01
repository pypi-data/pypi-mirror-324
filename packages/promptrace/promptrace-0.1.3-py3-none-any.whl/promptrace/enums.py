from enum import Enum

class TracerType(Enum):
    FILE = "file"
    DATABASE = "database"
    CONSOLE = "console"

class ModelType(Enum):
    AZURE_OPENAI = "azure_openai"
    DEEPSEEK = "deepseek"

class EvaluationMetric(Enum):
    IS_NUMERIC = "is_numeric"