import requests
from typing import Optional, List
from models.units import UnitsResponse, Unit
from api.auth import UCStudentAuth


class AcademicAPI:
    def __init__(self, auth: UCStudentAuth, language: str = 'pt'):
        self.auth = auth
        self.base_url = "https://academic.fw.uc.pt"
        self.language = language

    def get_units(self, academic_year: Optional[str] = None) -> UnitsResponse:
        """
        Fetch all units/courses for the authenticated student

        Args:
            academic_year: Optional academic year (e.g., "2025/2026").
                          If not provided, uses current academic year.

        Returns:
            UnitsResponse containing all units and metadata
        """
        if not self.auth.is_authenticated:
            raise Exception("Not authenticated. Please login first.")

        url = f"{self.base_url}/v2/student/units"

        # Get the session which already has Authorization header set
        session = self.auth.get_session()

        # Set all required headers for the academic API
        accept_language = "pt-PT" if self.language == 'pt' else "en-US"
        headers = {
            "Accept": "application/json",
            "Accept-Language": accept_language,
            "Referer": "https://ucstudent.uc.pt/",
            "Origin": "https://ucstudent.uc.pt",
            "Authorization": self.auth.token,
            "FwApp": "ucstudent|3.0.5|yef6rw",
            "Host": "academic.fw.uc.pt",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0"
        }

        params = {}
        if academic_year:
            params['academic_year'] = academic_year


        try:
            response = session.get(url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            return UnitsResponse(**data)

        except requests.RequestException as e:
            print(f"Error fetching units: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise

    def get_units_list(self, academic_year: Optional[str] = None) -> List[Unit]:
        """
        Get a simple list of units without metadata

        Returns:
            List of Unit objects
        """
        response = self.get_units(academic_year)
        return response.units

    def filter_units_by_course(self, course_key: str, academic_year: Optional[str] = None) -> List[Unit]:
        """
        Filter units by a specific course key

        Args:
            course_key: The course key to filter by
            academic_year: Optional academic year

        Returns:
            List of units belonging to the specified course
        """
        units = self.get_units_list(academic_year)
        return [unit for unit in units
                if any(course.key == course_key for course in unit.courses)]

    def get_unit_by_key(self, unit_key: str, academic_year: Optional[str] = None) -> Optional[Unit]:
        """
        Get a specific unit by its key

        Args:
            unit_key: The unit key to search for
            academic_year: Optional academic year

        Returns:
            Unit object if found, None otherwise
        """
        units = self.get_units_list(academic_year)
        for unit in units:
            if unit.key == unit_key:
                return unit
        return None

    def get_sessions(self) -> List[dict]:
        """
        Fetch upcoming class sessions for the authenticated student

        Returns:
            List of session dictionaries
        """
        if not self.auth.is_authenticated:
            raise Exception("Not authenticated. Please login first.")

        url = f"{self.base_url}/v1/student/sessions/next"

        # Get the session which already has Authorization header set
        session = self.auth.get_session()

        # Set all required headers for the academic API
        accept_language = "pt-PT" if self.language == 'pt' else "en-US"
        headers = {
            "Accept": "application/json",
            "Accept-Language": accept_language,
            "Referer": "https://ucstudent.uc.pt/",
            "Origin": "https://ucstudent.uc.pt",
            "Authorization": self.auth.token,
            "FwApp": "ucstudent|3.0.6|ujmvgi",
            "Host": "academic.fw.uc.pt",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0"
        }

        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            return data

        except requests.RequestException as e:
            print(f"Error fetching sessions: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise
