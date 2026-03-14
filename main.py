import os
import sys
from typing import List
from api.auth import UCStudentAuth
from api.academic import AcademicAPI
from api.buckets import BucketsAPI
from models.buckets import BucketItem

def sanitize_path(name: str) -> str:
    """Sanitize folder/file names for the filesystem"""
    return "".join(c for c in name if c.isalnum() or c in (' ', '.', '_', '-')).strip()

def download_recursive(buckets_api: BucketsAPI, bucket_key: str, local_path: str, folder_key: str = None):
    """Recursively download contents of a bucket/folder"""
    os.makedirs(local_path, exist_ok=True)
    
    try:
        bucket_detail = buckets_api.get_bucket_contents(bucket_key, folder_key)
    except Exception as e:
        print(f"  Error fetching contents for {local_path}: {e}")
        return

    for item in bucket_detail.items:
        item_path = os.path.join(local_path, sanitize_path(item.title))
        
        if item.type == 'folder':
            print(f"  Folder: {item.title}")
            download_recursive(buckets_api, bucket_key, item_path, item.key)
        elif item.type == 'file':
            if not os.path.exists(item_path):
                print(f"  Downloading: {item.title}")
                success = buckets_api.download_file(item, item_path)
                if not success:
                    print(f"    Failed to download {item.title}")
            else:
                # print(f"  Skipping (exists): {item.title}")
                pass

def main():
    username = os.environ.get("UC_USERNAME")
    password = os.environ.get("UC_PASSWORD")
    download_dir = os.environ.get("DOWNLOAD_DIR", ".")

    if not username or not password:
        print("Error: Missing UC_USERNAME or UC_PASSWORD environment variables.")
        sys.exit(1)

    auth = UCStudentAuth()
    print("Logging in...")
    if not auth.login(username, password):
        print("Login failed.")
        sys.exit(1)

    print("Login successful!")
    
    academic_api = AcademicAPI(auth)
    buckets_api = BucketsAPI(auth)

    try:
        units_response = academic_api.get_units()
        academic_year = units_response.academic_year or "unknown_year"
        print(f"Fetching units for {academic_year}...")
        
        for unit in units_response.units:
            print(f"\nUnit: {unit.title} ({unit.key})")
            
            # Use the first course key as a top-level folder
            course_name = sanitize_path(unit.courses[0].title) if unit.courses else "Unknown Course"
            unit_name = sanitize_path(unit.title)
            
            # Place files at root if download_dir is '.'
            if download_dir == ".":
                unit_path = os.path.join(sanitize_path(academic_year), course_name, unit_name)
            else:
                unit_path = os.path.join(download_dir, sanitize_path(academic_year), course_name, unit_name)
            
            buckets = buckets_api.get_buckets_for_unit(unit.unit_key_for_bucket, unit.key)
            for bucket in buckets:
                print(f" Bucket: {bucket.title}")
                bucket_path = os.path.join(unit_path, sanitize_path(bucket.title))
                download_recursive(buckets_api, bucket.key, bucket_path)

    except Exception as e:
        print(f"An error occurred during sync: {e}")
    finally:
        auth.logout()
        print("\nSync complete. Logged out.")

if __name__ == "__main__":
    main()
