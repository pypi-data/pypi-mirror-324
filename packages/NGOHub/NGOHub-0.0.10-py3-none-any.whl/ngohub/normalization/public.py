from typing import Dict

from ngohub.models.public import Version


def normalize_version(version_data: Dict[str, str]) -> Version:
    normal_data = Version(**version_data)

    return normal_data
