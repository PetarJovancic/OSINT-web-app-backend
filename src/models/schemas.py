from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ScanRequest(BaseModel):
    scan_type: str
    website: str 

    class Config:
        json_schema_extra = {
            "example": {
                "scan_type": "THE_HARVESTER",
                "website": "google.com"
            }
        }

class ScanResultWithIPs(BaseModel):
    id: str
    scan_type: str
    website: str
    status: str
    target: str
    created_at: datetime
    completed_at: datetime
    ips: List[str]
    subdomains: List[str]
    emails: List[str]
    error: Optional[str] = None

    class Config:
        from_attributes = True

class ScanResultID(BaseModel):
    id: str

class ScanResultIDs(BaseModel):
    ids: List[ScanResultID]

    class Config:
        from_attributes = True

class ScanResult(BaseModel):
    target: str
    total_ips: int
    ips: List[str]
    emails: List[str] 
    total_hosts: int 
    subdomains: List[str]

class ScanStatus(BaseModel):
    id: str
    type: str
    website: str
    status: str
    results: ScanResult
    created_at: datetime 
    completed_at: Optional[datetime] = None

class ScanResults(BaseModel):
    id: str
    scan_type: str
    website: str
    status: str
    created_at: datetime
    completed_at: datetime
    error: Optional[str] = None