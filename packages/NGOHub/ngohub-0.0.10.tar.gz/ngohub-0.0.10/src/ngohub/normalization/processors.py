import re
from datetime import datetime
from re import Pattern
from typing import Any, Dict, List, Optional

camel_case_to_snake_case_pattern: Optional[Pattern[str]] = None


def _compile_camel_to_snake_case_pattern() -> Pattern[str]:
    global camel_case_to_snake_case_pattern

    if not camel_case_to_snake_case_pattern:
        camel_case_to_snake_case_pattern = re.compile(
            r"""
                (?<=[a-z])      # preceded by lowercase
                (?=[A-Z])       # followed by uppercase
                |               #   OR
                (?<=[A-Z])      # preceded by uppercase
                (?=[A-Z][a-z])  # followed by uppercase, then lowercase
            """,
            re.X,
        )

    return camel_case_to_snake_case_pattern


def camel_to_snake_case(input_string: str) -> str:
    pattern: Pattern[str] = _compile_camel_to_snake_case_pattern()

    return pattern.sub("_", input_string).lower()


def camel_to_snake_case_dictionary(
    input_dict: Dict[str, Any],
    overrides: Dict[str, Any] = None,
    cast_values: Dict[str, Any] = None,
) -> Dict[str, Any]:
    output_dict: Dict[str, Any] = {}

    for old_key, value in input_dict.items():
        if overrides and old_key in overrides:
            new_key = overrides[old_key]
        else:
            new_key = camel_to_snake_case(old_key)

        if new_key in output_dict:
            raise ValueError(f"Cannot normalize {old_key} to {new_key} because { new_key} already exists")

        if cast_values and new_key in cast_values:
            value = cast_values[new_key](value)
        elif isinstance(value, dict):
            value = camel_to_snake_case_dictionary(value, overrides, cast_values)
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            value = camel_to_snake_case_dictionary_list(value, overrides, cast_values)

        output_dict[new_key] = value

    return output_dict


def camel_to_snake_case_dictionary_list(
    input_list: List[Dict[str, Any]],
    overrides: Dict[str, Any] = None,
    cast_values: Dict[str, Any] = None,
) -> List[Dict[str, Any]]:
    return [camel_to_snake_case_dictionary(item, overrides, cast_values) for item in input_list]


def convert_date(date: str) -> Optional[datetime]:
    if not date:
        return None

    return datetime.fromisoformat(date)
