import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin
import json

class UCStudentAuth:
    def __init__(self, base_url: str = "https://ucstudent.uc.pt"):
        self.base_url = base_url
        self.auth_url = "https://id.fw.uc.pt"
        self.session = requests.Session()
        self.is_authenticated = False
        self.user_data = None
        self.token = None
        self.user_token = None

    def login(self, username: str, password: str) -> bool:
        """
        Authenticate with UCStudent platform

        Args:
            username: UCStudent username (email or student number)
            password: UCStudent password

        Returns:
            bool: True if login successful, False otherwise
        """

        # Add @student.uc.pt if only student number provided
        if '@' not in username:
            # Check if it's a student number (starts with uc followed by year and number)
            if username.startswith('uc'):
                username = f"{username}@student.uc.pt"
            else:
                username = f"uc{username}@student.uc.pt"

        login_url = f"{self.auth_url}/v1/login"

        payload = {
            "email": username,
            "password": password,
            "longLivedToken": True,
            "callbackApp": None
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "FwApp": "ucstudent|3.0.5|qpjy4h",
            "Origin": "https://ucstudent.uc.pt",
            "Referer": "https://ucstudent.uc.pt/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0"
        }

        try:
            response = self.session.post(
                login_url,
                json=payload,
                headers=headers,
                allow_redirects=False
            )

            if response.status_code == 200:
                data = response.json()
                self.is_authenticated = True
                self.token = data.get('token')
                self.user_data = data.get('user', {})
                self.user_token = self.user_data.get('token')


                # Set headers for future requests - Authorization without Bearer prefix
                self.session.headers['Authorization'] = self.token
                self.session.headers['FwApp'] = "ucstudent|3.0.5|qpjy4h"

                return True
            else:
                print(f"Login failed with status: {response.status_code}")
                if response.text:
                    print(f"Response: {response.text}")
                return False

        except requests.RequestException as e:
            print(f"Login error: {e}")
            return False

    def logout(self) -> None:
        """Logout and clear session"""
        try:
            logout_url = urljoin(self.base_url, "/api/auth/logout")
            self.session.post(logout_url)
        except:
            pass
        finally:
            self.session.close()
            self.session = requests.Session()
            self.is_authenticated = False
            self.user_data = None
            self.token = None
            self.user_token = None

    def get_user_info(self) -> Dict[str, Any]:
        """Get the authenticated user's information"""
        if not self.is_authenticated:
            return {}
        return self.user_data or {}

    def test_connection(self) -> bool:
        """Test if we can reach UCStudent"""
        try:
            response = self.session.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_session(self) -> requests.Session:
        """Get the authenticated session for making API calls"""
        if not self.is_authenticated:
            raise Exception("Not authenticated. Please login first.")
        return self.session
