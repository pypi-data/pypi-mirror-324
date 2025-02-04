from typing import Any, Dict, List

from ngohub.models.locations import City, CityBase, County, Region
from ngohub.models.nomenclatures import Domain
from ngohub.models.organization import (
    Application,
    Organization,
    OrganizationActivity,
    OrganizationApplication,
    OrganizationContact,
    OrganizationDirector,
    OrganizationFinancial,
    OrganizationGeneral,
    OrganizationInvestors,
    OrganizationLegal,
    OrganizationLegalReprezentative,
    OrganizationPartners,
    OrganizationReport,
    OrganizationReports,
)
from ngohub.normalization.processors import (
    camel_to_snake_case_dictionary,
    camel_to_snake_case_dictionary_list,
    convert_date,
)


def _normalize_city(city_data: Dict) -> City:
    city_data["county"] = County(**city_data["county"])

    normal_data = City(**city_data)

    return normal_data


def _normalize_organization_general(org_general_data: Dict) -> OrganizationGeneral:
    org_general_data["contact"] = OrganizationContact(**org_general_data["contact"])

    org_general_data["city"] = CityBase(**org_general_data["city"])
    org_general_data["county"] = County(**org_general_data["county"])

    if org_general_data["organization_city"]:
        org_general_data["organization_city"] = CityBase(**org_general_data["organization_city"])
    if org_general_data["organization_county"]:
        org_general_data["organization_county"] = County(**org_general_data["organization_county"])

    org_general = OrganizationGeneral(**org_general_data)

    return org_general


def _normalize_organization_activity(org_activity_data: Dict) -> OrganizationActivity:
    org_domains: List[Domain] = []
    org_regions: List[Region] = []
    org_cities: List[City] = []

    for domain in org_activity_data["domains"]:
        org_domains.append(Domain(**domain))
    for region in org_activity_data["regions"]:
        org_regions.append(Region(**region))
    for city in org_activity_data["cities"]:
        org_cities.append(_normalize_city(city))

    org_activity_data["domains"] = org_domains
    org_activity_data["regions"] = org_regions
    org_activity_data["cities"] = org_cities

    normal_data = OrganizationActivity(**org_activity_data)

    return normal_data


def _normalize_organization_legal(org_legal_data: Dict) -> OrganizationLegal:
    org_directors: List[OrganizationDirector] = []
    for director in org_legal_data["directors"]:
        org_directors.append(OrganizationDirector(**director))

    org_legal_data["directors"] = org_directors
    org_legal_data["legal_reprezentative"] = OrganizationLegalReprezentative(**org_legal_data["legal_reprezentative"])

    normal_data = OrganizationLegal(**org_legal_data)

    return normal_data


def _normalize_organization_financial(org_financial_data_set: List[Dict]) -> List[OrganizationFinancial]:
    normal_data = [OrganizationFinancial(**org_financial_data) for org_financial_data in org_financial_data_set]

    return normal_data


def _normalize_organization_report(org_report_data: Dict) -> OrganizationReport:
    org_reports: List[OrganizationReports] = []
    org_partners: List[OrganizationPartners] = []
    org_investors: List[OrganizationInvestors] = []

    for report in org_report_data.get("reports"):
        org_reports.append(OrganizationReports(**report))

    for partner in org_report_data.get("partners"):
        org_partners.append(OrganizationPartners(**partner))

    for investor in org_report_data.get("investors"):
        org_investors.append(OrganizationInvestors(**investor))

    org_report_data["reports"] = org_reports
    org_report_data["partners"] = org_partners
    org_report_data["investors"] = org_investors

    normal_data = OrganizationReport(**org_report_data)

    return normal_data


def normalize_organization_data(org_data: Dict) -> Organization:
    snake_case: Dict[str, any] = camel_to_snake_case_dictionary(
        org_data,
        overrides={
            "isPublicIntrestOrganization": "is_public_interest_organization",
            "synched_anaf": "synced_anaf",
            "organizationGeneral": "general_data",
            "organizationActivity": "activity_data",
            "organizationLegal": "legal_data",
            "organizationFinancial": "financial_data",
            "organizationReport": "report_data",
        },
        cast_values={"created_on": convert_date, "updated_on": convert_date},
    )

    snake_case["general_data"] = _normalize_organization_general(snake_case["general_data"])
    snake_case["activity_data"] = _normalize_organization_activity(snake_case["activity_data"])
    snake_case["legal_data"] = _normalize_organization_legal(snake_case["legal_data"])
    snake_case["financial_data"] = _normalize_organization_financial(snake_case["financial_data"])
    snake_case["report_data"] = _normalize_organization_report(snake_case["report_data"])

    normal_data = Organization(**snake_case)

    return normal_data


def normalize_organization_applications(org_data_set: List[Dict[str, Any]]) -> List[OrganizationApplication]:
    snake_case_response: List[Dict[str, any]] = camel_to_snake_case_dictionary_list(
        org_data_set,
        overrides={"ongStatus": "ngo_status"},
        cast_values={"created_on": convert_date},
    )

    normal_data: List[OrganizationApplication] = [
        OrganizationApplication(**org_data) for org_data in snake_case_response
    ]

    return normal_data


def normalize_application_list(application_data_set: List[Dict]) -> List[Application]:
    snake_case_response: List[Dict[str, any]] = camel_to_snake_case_dictionary_list(application_data_set)

    normal_data: List[Application] = [Application(**app_data) for app_data in snake_case_response]

    return normal_data
