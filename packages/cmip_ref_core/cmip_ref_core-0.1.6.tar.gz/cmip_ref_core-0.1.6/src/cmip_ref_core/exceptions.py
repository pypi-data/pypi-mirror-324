import pathlib
from typing import Any


class RefException(Exception):
    """Base class for exceptions related to REF operations"""

    pass


class InvalidMetricException(RefException):
    """Exception raised when an invalid metric is registered"""

    def __init__(self, metric: Any, message: str) -> None:
        message = f"Invalid metric: '{metric}'\n {message}"

        super().__init__(message)


class OutOfTreeDatasetException(RefException):
    """Exception raised when a dataset is not in the datatree"""

    def __init__(self, dataset_path: pathlib.Path, root_path: pathlib.Path) -> None:
        message = (
            f"Dataset: '{dataset_path}' is not in the datatree: '{root_path}'\n"
            "To opt-in to this behaviour set the configuration value "
            "'paths.allow_out_of_tree_datasets' to True"
        )

        super().__init__(message)


class ConstraintNotSatisfied(RefException):
    """Exception raised when a constraint is violated"""

    # TODO: implement when we have agreed on using constraints
