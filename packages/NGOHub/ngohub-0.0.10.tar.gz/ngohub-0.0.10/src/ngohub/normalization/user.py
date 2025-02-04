from typing import Any, Dict

from ngohub.models.organization import OrganizationBase
from ngohub.models.user import User, UserProfile
from ngohub.normalization.processors import camel_to_snake_case_dictionary


def normalize_user(user_data: Dict[str, Any]) -> User:
    normal_data = User(
        id=user_data["id"],
        created_on=user_data["createdOn"],
        updated_on=user_data["updatedOn"],
        cognito_id=user_data["cognitoId"],
        name=user_data["name"],
        email=user_data["email"],
        phone=user_data["phone"],
        role=user_data["role"],
        status=user_data["status"],
        organization_id=user_data["organizationId"],
    )

    return normal_data


def normalize_user_profile(user_data: Dict[str, Any]) -> UserProfile:
    snake_case: Dict[str, any] = camel_to_snake_case_dictionary(user_data)

    if snake_case["organization"]:
        snake_case["organization"] = OrganizationBase(**snake_case["organization"])

    normal_data = UserProfile(**snake_case)

    return normal_data
