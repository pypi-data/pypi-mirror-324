from dataclasses import dataclass
from datetime import datetime

from ngohub.models.core import BaseDataclass


@dataclass
class BaseEntity(BaseDataclass):
    id = int
    created_on = datetime
    updated_on = datetime
    name = str
    abbreviation = str


@dataclass
class Federation(BaseEntity): ...


@dataclass
class Coalition(BaseEntity): ...
