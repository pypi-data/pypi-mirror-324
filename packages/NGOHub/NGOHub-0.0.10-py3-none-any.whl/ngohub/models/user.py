from dataclasses import dataclass
from datetime import datetime
from typing import Union

from ngohub.models.core import BaseDataclass
from ngohub.models.organization import OrganizationBase


@dataclass
class BaseUser(BaseDataclass):
    id: int
    created_on: datetime
    updated_on: datetime
    cognito_id: str
    name: str
    email: str
    phone: str
    role: str
    status: str


@dataclass
class User(BaseUser):
    organization_id: int


@dataclass
class UserProfile(BaseUser):
    organization: Union[OrganizationBase, None]
