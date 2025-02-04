from dataclasses import dataclass

from ngohub.models.core import BaseDataclass


@dataclass
class Version(BaseDataclass):
    version: str
    revision: str
