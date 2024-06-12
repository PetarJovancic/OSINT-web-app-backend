from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from src.models.schemas import ScanRequest, ScanStatus, ScanResultWithIPs, ScanResultIDs, ScanResults
from src.config.database import get_db
from src.services.scan_services import get_all_ids, get_results, run_scan, get_scans


router = APIRouter()


@router.post("/scan", response_model=ScanStatus)
async def create_scan(scan_request: ScanRequest, db: Session = Depends(get_db)) -> ScanStatus:
    results = await run_scan(scan_request, db)
    return results

@router.get("/ids", response_model=ScanResultIDs)
async def get_all_scan_ids(db: Session = Depends(get_db)) -> ScanResultIDs:
    results = await get_all_ids(db)
    return results

@router.get("/scan/{scan_id}", response_model=ScanResultWithIPs)
async def get_scan_results(scan_id: str, db: Session = Depends(get_db)):
    results = await get_results(scan_id, db)
    return results

@router.get("/scan", response_model=list[ScanResults])
async def get_all_scans(db: Session = Depends(get_db)):
    results = await get_scans(db)
    return results