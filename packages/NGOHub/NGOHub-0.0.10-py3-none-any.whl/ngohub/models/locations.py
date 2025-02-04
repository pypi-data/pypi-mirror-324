from dataclasses import dataclass
from datetime import datetime

from ngohub.models.core import BaseDataclass


@dataclass
class Region(BaseDataclass):
    id: int
    name: str
    created_on: datetime
    updated_on: datetime


@dataclass
class County(BaseDataclass):
    id: int
    name: str
    abbreviation: str
    region_id: int
    created_on: datetime


@dataclass
class CityBase(BaseDataclass):
    id: int
    name: str
    created_on: datetime
    county_id: int


@dataclass
class City(CityBase):
    county: County
