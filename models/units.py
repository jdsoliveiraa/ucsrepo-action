from dataclasses import dataclass, field
from typing import List, Optional, Any

@dataclass
class Course:
    key: str
    title: str
    
    def __init__(self, **kwargs):
        self.key = kwargs.get('key')
        self.title = kwargs.get('title')

@dataclass
class Unit:
    key: str
    title: str
    unit_key_for_bucket: str
    courses: List[Course] = field(default_factory=list)
    
    def __init__(self, **kwargs):
        self.key = kwargs.get('key')
        self.title = kwargs.get('title')
        self.unit_key_for_bucket = kwargs.get('unit_key_for_bucket')
        self.courses = [Course(**c) for c in kwargs.get('courses', [])]

@dataclass
class UnitsResponse:
    units: List[Unit] = field(default_factory=list)
    academic_year: Optional[str] = None
    
    def __init__(self, **kwargs):
        self.units = [Unit(**u) for u in kwargs.get('units', [])]
        self.academic_year = kwargs.get('academic_year')
