from dataclasses import dataclass, field
from typing import List, Optional, Any

@dataclass
class FileInfo:
    url_format: str
    token: str
    key: str
    filename: str
    
    def __init__(self, **kwargs):
        self.url_format = kwargs.get('url_format')
        self.token = kwargs.get('token')
        self.key = kwargs.get('key')
        self.filename = kwargs.get('filename')

@dataclass
class BucketItem:
    title: str
    type: str  # 'file' or 'folder'
    key: str
    file: Optional[FileInfo] = None
    
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.type = kwargs.get('type')
        self.key = kwargs.get('key')
        file_data = kwargs.get('file')
        if file_data:
            self.file = FileInfo(**file_data)
        else:
            self.file = None

@dataclass
class BucketDetail:
    key: str
    title: str
    items: List[BucketItem] = field(default_factory=list)
    
    def __init__(self, **kwargs):
        self.key = kwargs.get('key')
        self.title = kwargs.get('title')
        self.items = [BucketItem(**item) for item in kwargs.get('items', [])]

@dataclass
class Bucket:
    key: str
    title: str
    type: str
    unit_key_for_bucket: Optional[str] = None
    
    def __init__(self, **kwargs):
        self.key = kwargs.get('key')
        self.title = kwargs.get('title')
        self.type = kwargs.get('type')
        # Some buckets might have extra info
        self.unit_key_for_bucket = kwargs.get('unit_key_for_bucket')
