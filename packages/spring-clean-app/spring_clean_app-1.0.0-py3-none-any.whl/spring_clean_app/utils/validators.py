# Define an interface
import re
from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    """Abstract base class for validators."""

    def __init__(self, error_message: str):
        self.error_message = f"❌ {error_message}"

    @abstractmethod
    def validate(self, value: Any) -> bool:
        """Abstract method that must be implemented by subclasses."""
        pass


class ExistedValuesValidator(Validator):
    def __init__(self, valid_values, error_message="Invalid value!"):
        super().__init__(error_message)
        self.valid_values = valid_values  # List of allowed values

    def validate(self, value: Any) -> bool:
        """Checks if the value exists in the valid values list."""
        return value in self.valid_values


class RegexValidator(Validator):
    def __init__(self, regex, error_message="Invalid value!"):
        super().__init__(error_message)
        self.regex = regex
        self.pattern = re.compile(regex)

    def validate(self, value: Any) -> bool:
        return bool(self.pattern.fullmatch(str(value)))
