from dataclasses import dataclass
from datetime import datetime

from ngohub.models.core import BaseDataclass


@dataclass
class Domain(BaseDataclass):
    id: int
    name: str
    created_on: datetime
    updated_on: datetime
