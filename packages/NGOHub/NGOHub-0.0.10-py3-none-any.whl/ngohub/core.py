from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from ngohub.exceptions import HubHTTPException, MissingUserException
from ngohub.models.checks import CheckOrganizationUserApplication
from ngohub.models.organization import Application, Organization, OrganizationApplication
from ngohub.models.public import Version
from ngohub.models.user import User, UserProfile
from ngohub.network import HTTPClient, HTTPClientResponse
from ngohub.normalization.organization import (
    normalize_application_list,
    normalize_organization_applications,
    normalize_organization_data,
)
from ngohub.normalization.public import normalize_version
from ngohub.normalization.user import normalize_user, normalize_user_profile


class BaseHub(ABC):
    """
    Abstract class used to define all the required methods for a hub interface
    """

    @abstractmethod
    def __init__(self, api_base_url: str) -> None:
        self.api_base_url: str = api_base_url or ""


class NGOHubRaw(BaseHub):
    def __init__(self, api_base_url: str) -> None:
        super().__init__(api_base_url)

        self.client: HTTPClient = HTTPClient(self.api_base_url)

    def get_raw_health(self) -> str:
        response: HTTPClientResponse = self.client.api_get("/health/")

        return response.to_str()

    def get_raw_version(self) -> Dict[str, str]:
        response: HTTPClientResponse = self.client.api_get("/version/")

        return response.to_dict()

    def get_raw_file_url(self, path: str) -> str:
        url_params: Dict[str, str] = {"path": path}
        response: HTTPClientResponse = self.client.api_get(f"/file?{urlencode(url_params)}")

        return response.to_str()

    def _get_raw_nomenclature(self, nomenclature: str) -> Any:
        response: HTTPClientResponse = self.client.api_get(f"/nomenclatures/{nomenclature}")

        return response.to_dict()

    def get_raw_cities_nomenclatures(
        self, search: str = None, county_id: int = None, city_id: int = None
    ) -> List[Dict[str, Any]]:
        mandatory_params: List[Any] = [search, county_id]
        if all(param is None for param in mandatory_params):
            raise ValueError("Please provide at least one of the following: county_id, search")

        url_params: Dict[str, Any] = {}
        if search:
            url_params["search"] = search
        if county_id:
            url_params["countyId"] = county_id
        if city_id:
            url_params["cityId"] = city_id

        return self._get_raw_nomenclature(f"cities?{urlencode(url_params)}")

    def get_raw_counties_nomenclatures(self) -> List[Dict[str, Any]]:
        return self._get_raw_nomenclature("counties")

    def get_raw_domains_nomenclatures(self):
        return self._get_raw_nomenclature("domains")

    def get_raw_regions_nomenclatures(self):
        return self._get_raw_nomenclature("regions")

    def get_raw_federations_nomenclatures(self):
        return self._get_raw_nomenclature("federations")

    def get_raw_coalitions_nomenclatures(self):
        return self._get_raw_nomenclature("coalitions")

    def get_raw_faculties_nomenclatures(self):
        return self._get_raw_nomenclature("faculties")

    def get_raw_skills_nomenclatures(self):
        return self._get_raw_nomenclature("skills")

    def get_raw_practice_domains_nomenclatures(self):
        return self._get_raw_nomenclature("practice-domains")

    def get_raw_service_domains_nomenclatures(self):
        return self._get_raw_nomenclature("service-domains")

    def get_raw_beneficiaries_nomenclatures(self):
        return self._get_raw_nomenclature("beneficiaries")

    def get_raw_issuers_nomenclatures(self):
        return self._get_raw_nomenclature("issuers")

    def get_raw_profile(self, user_token: str) -> Dict[str, Any]:
        response: HTTPClientResponse = self.client.api_get("/profile/", token=user_token)

        return response.to_dict()

    def get_raw_organization_profile(self, ngo_token: str) -> Dict[str, Any]:
        response: HTTPClientResponse = self.client.api_get("/organization-profile/", token=ngo_token)

        return response.to_dict()

    def get_raw_application_list(self, admin_token: str) -> List[Dict[str, Any]]:
        response: HTTPClientResponse = self.client.api_get("/application/list/", token=admin_token)

        return list(response.to_dict())

    def get_raw_user_organization_applications(self, ngo_token: str) -> List[Dict[str, Any]]:
        response: HTTPClientResponse = self.client.api_get("/organizations/application/", token=ngo_token)

        return list(response.to_dict())

    def get_raw_organization(self, admin_token: str, organization_id: int) -> Dict[str, Any]:
        response: HTTPClientResponse = self.client.api_get(f"/organization/{organization_id}/", token=admin_token)

        return response.to_dict()

    def get_raw_organization_applications(self, admin_token, organization_id) -> List[Dict[str, Any]]:
        response: HTTPClientResponse = self.client.api_get(
            f"/application/organization/{organization_id}/", token=admin_token
        )
        return list(response.to_dict())

    def get_user_raw(self, admin_token: str, user_id: int) -> Dict[str, Any]:
        try:
            response: HTTPClientResponse = self.client.api_get(f"/user/{user_id}/", token=admin_token)
        except HubHTTPException as e:
            if e.status_code == 404:
                raise MissingUserException(f"User with ID {user_id} not found")

            raise e

        return response.to_dict()

    def get_raw_users(
        self,
        admin_token: str,
        organization_id: int,
        limit: int = 1000,
        page: int = 1,
        search: str = None,
        order_by: str = None,
        order_direction: str = None,
        start: str = None,
        end: str = None,
        status: str = None,
        available_apps_ids: List[int] = None,
    ) -> Dict[str, Any]:
        base_url: str = "/user"
        url_params: dict = {"organization_id": organization_id, "limit": limit, "page": page}

        if search:
            url_params["search"] = search

        if order_by:
            url_params["orderBy"] = order_by
        if order_direction and order_direction.upper() in ["ASC", "DESC"]:
            url_params["orderDirection"] = order_direction.upper()

        if start:
            url_params["start"] = start
        if end:
            url_params["end"] = end

        if status and status.lower() in ["active", "pending", "restricted"]:
            url_params["status"] = status.lower()

        if available_apps_ids:
            url_params["availableAppsIDs"] = [str(app_id) for app_id in available_apps_ids]

        request_url: str = f"{base_url}?{urlencode(url_params)}"
        response: HTTPClientResponse = self.client.api_get(request_url, token=admin_token)

        return response.to_dict()


class NGOHub(NGOHubRaw):
    def __init__(self, api_base_url: str) -> None:
        super().__init__(api_base_url)

    def is_healthy(self) -> bool:
        return bool(self.get_raw_health() == "OK")

    def get_version(self) -> Version:
        return normalize_version(self.get_raw_version())

    def get_file_url(self, path: str) -> str:
        return self.get_raw_file_url(path)

    def get_profile(self, user_token: str) -> UserProfile:
        response: Dict[str, Any] = self.get_raw_profile(user_token=user_token)

        return normalize_user_profile(response)

    # Organization related methods
    def get_organization_profile(self, ngo_token: str) -> Organization:
        response: Dict[str, Any] = self.get_raw_organization_profile(ngo_token)

        return normalize_organization_data(response)

    def get_user_organization_applications(self, ngo_token: str) -> List[OrganizationApplication]:
        response: List[Dict[str, Any]] = self.get_raw_user_organization_applications(ngo_token)

        return normalize_organization_applications(response)

    def check_user_organization_has_application(
        self, ngo_token: str, login_link: str
    ) -> Union[OrganizationApplication, None]:
        organization_applications: List[OrganizationApplication] = self.get_user_organization_applications(ngo_token)

        for app in organization_applications:
            if app.login_link.startswith(login_link) and app.status == "active" and app.ngo_status == "active":
                return app

        return None

    # Admin related methods
    def get_application_list(self, admin_token: str) -> List[Application]:
        response: List[Dict[str, Any]] = self.get_raw_application_list(admin_token)

        return normalize_application_list(response)

    def get_organization(self, admin_token: str, organization_id: int) -> Organization:
        response: Dict[str, Any] = self.get_raw_organization(admin_token=admin_token, organization_id=organization_id)

        return normalize_organization_data(response)

    def get_organization_applications(self, admin_token: str, organization_id: int) -> List[OrganizationApplication]:
        response = self.get_raw_organization_applications(admin_token, organization_id)

        return normalize_organization_applications(response)

    def get_user(self, admin_token: str, user_id: int) -> User:
        response: Dict[str, Any] = self.get_user_raw(admin_token, user_id)

        return normalize_user(response)

    def check_organization_has_application(
        self, admin_token: str, organization_id: int, login_link: str
    ) -> Optional[OrganizationApplication]:
        organization_applications: List[OrganizationApplication] = self.get_organization_applications(
            admin_token, organization_id
        )

        for application in organization_applications:
            if (
                application.login_link.startswith(login_link)
                and application.status == "active"
                and application.ngo_status == "active"
            ):
                return application

        return None

    def _check_user_has_application(
        self, admin_token: str, organization_id: int, user_id: int, response: CheckOrganizationUserApplication
    ) -> CheckOrganizationUserApplication:
        continue_searching: bool = True
        page: int = 1

        searched_application_id = response.application.id

        while continue_searching:
            organization_users: Dict[str, Union[Dict, List]] = self.get_raw_users(
                admin_token=admin_token, organization_id=organization_id, page=page
            )

            response_metadata = organization_users.get("meta", {})
            response_users = organization_users.get("items", [])

            if response_metadata["totalPages"] <= response_metadata["currentPage"]:
                continue_searching = False
            else:
                page += 1

            for user in response_users:
                if user["id"] == int(user_id):
                    response.user = user
                    user_applications: List[Dict[str, Any]] = user["availableAppsIDs"]

                    if searched_application_id in user_applications:
                        response.has_access = True
                        return response

                    response.has_access = False
                    return response

        return response

    def check_organization_user_has_application(
        self,
        admin_token: str,
        organization_id: int,
        user_id: int,
        login_link: str,
    ) -> CheckOrganizationUserApplication:

        response: CheckOrganizationUserApplication = CheckOrganizationUserApplication()

        organization_application: OrganizationApplication = self.check_organization_has_application(
            admin_token, organization_id, login_link
        )
        if not organization_application:
            return response

        response.application = organization_application

        try:
            user: User = self.get_user(admin_token, user_id)
        except MissingUserException:
            return response

        if not user or user.organization_id != int(organization_id):
            return response

        response.user = user

        if user.role == "admin":
            response.has_access = True

            return response

        response = self._check_user_has_application(admin_token, organization_id, user_id, response)

        return response
