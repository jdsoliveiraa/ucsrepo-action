import requests
from typing import List, Optional
from urllib.parse import quote
from models.buckets import Bucket, BucketDetail, BucketItem
from api.auth import UCStudentAuth


class BucketsAPI:
    def __init__(self, auth: UCStudentAuth, language: str = 'pt'):
        self.auth = auth
        self.base_url = "https://buckets.fw.uc.pt"
        self.language = language

    def get_buckets_for_unit(self, unit_key_for_bucket: str, unit_key: str = None, class_key: str = None) -> List[Bucket]:
        """
        Get buckets for a specific unit

        Args:
            unit_key_for_bucket: The unit_key_for_bucket from Unit model (e.g., "267643")
            unit_key: Optional unit edition key (e.g., "yckasf")
            class_key: Optional class edition key

        Returns:
            List of buckets for the unit
        """
        if not self.auth.is_authenticated:
            raise Exception("Not authenticated. Please login first.")

        url = f"{self.base_url}/v1/buckets"

        # Build filters
        filters = []
        filters.append(f"filter=academic,unit,{unit_key_for_bucket}")

        if unit_key:
            filters.append(f"filter=academic,unit_edition,{unit_key}")

        if class_key:
            filters.append(f"filter=academic,class_edition,{class_key}")

        # Add filters to URL
        if filters:
            url += "?" + "&".join(filters)

        accept_language = "pt-PT" if self.language == 'pt' else "en-US"
        headers = {
            "Accept": "application/json",
            "Accept-Language": accept_language,
            "Authorization": self.auth.token,
            "FwApp": "ucstudent|3.0.5|w8m45x",
            "Origin": "https://ucstudent.uc.pt",
            "Referer": "https://ucstudent.uc.pt/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0"
        }

        try:
            session = self.auth.get_session()
            response = session.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            return [Bucket(**item) for item in data]

        except requests.RequestException as e:
            print(f"Error fetching buckets: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise

    def get_bucket_contents(self, bucket_key: str, folder_key: str = None) -> BucketDetail:
        """
        Get contents of a specific bucket or folder within a bucket

        Args:
            bucket_key: The bucket key
            folder_key: Optional folder key to get contents of a specific folder

        Returns:
            BucketDetail with all files in the bucket/folder
        """
        if not self.auth.is_authenticated:
            raise Exception("Not authenticated. Please login first.")

        url = f"{self.base_url}/v1/bucket/{bucket_key}"

        # Add folder_key as query parameter if provided
        if folder_key:
            url += f"?folder_key={folder_key}"

        accept_language = "pt-PT" if self.language == 'pt' else "en-US"
        headers = {
            "Accept": "application/json",
            "Accept-Language": accept_language,
            "Authorization": self.auth.token,
            "FwApp": "ucstudent|3.0.5|w8m45x",
            "Origin": "https://ucstudent.uc.pt",
            "Referer": "https://ucstudent.uc.pt/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0"
        }

        try:
            session = self.auth.get_session()
            response = session.get(url, headers=headers)
            response.raise_for_status()

            return BucketDetail(**response.json())

        except requests.RequestException as e:
            print(f"Error fetching bucket contents: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise

    def download_file(self, file_item: BucketItem, download_path: str) -> bool:
        """
        Download a file from a bucket

        Args:
            file_item: The BucketItem to download
            download_path: Local path to save the file

        Returns:
            True if download successful
        """
        if not self.auth.is_authenticated:
            raise Exception("Not authenticated. Please login first.")

        # Build download URL using the url_format
        # Format: https://storage.fw.uc.pt/f/{TOKEN}/{KEY}/{FILENAME}
        download_url = file_item.file.url_format.replace(
            "{TOKEN}", file_item.file.token
        ).replace(
            "{KEY}", file_item.file.key
        ).replace(
            "{FILENAME}", quote(file_item.file.filename)
        )

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0"
        }

        try:
            response = requests.get(download_url, headers=headers, stream=True)
            response.raise_for_status()

            # Write file to disk
            with open(download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            return True

        except requests.RequestException as e:
            print(f"Error downloading file {file_item.title}: {e}")
            return False
