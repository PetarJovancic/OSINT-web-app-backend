import docker
import logging
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from fastapi import HTTPException

from src.models.schemas import ScanRequest, ScanStatus, ScanResultWithIPs, ScanResultIDs, ScanResultID
from src.models.models import ScanResultModel, IPModel, EmailModel, SubdomainModel
from src.utils.parser import parse_theharvester_output
from src.utils.scanner import run_amass_scan, run_theharvester_scan


logging.basicConfig(level=logging.INFO)
client = docker.from_env()

async def get_all_ids(db: Session) -> ScanResultIDs:
    try:
        scan_ids = db.query(ScanResultModel.id).all()
        return ScanResultIDs(ids=[ScanResultID(id=scan_id[0]) for scan_id in scan_ids])
    except Exception as e:
        logging.exception(f"Error fetching scan result IDs: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def run_scan(scan_request: ScanRequest, db: Session) -> ScanStatus:
    scan_id = str(uuid4())
    start_time = datetime.now()
    
    try:
        if scan_request.scan_type == "THE_HARVESTER":
            output = await run_theharvester_scan(scan_request.website)
        elif scan_request.scan_type == "AMASS":
            output = await run_amass_scan(scan_request.website)
        else:
            raise HTTPException(status_code=400, detail="Invalid scan type")

        logging.info(f"Scan output: {output}")

        parsed_results = parse_theharvester_output(output)
        
        scan_result = ScanResultModel(
            id=scan_id,
            scan_type=scan_request.scan_type,
            website=scan_request.website,
            status="Completed",
            target=parsed_results.target,
            created_at=start_time,
            completed_at=datetime.now()
        )

        db.add(scan_result)
        db.commit()

        subdomain_mappings = [{"scan_id": scan_id, "subdomain": subdomain} for subdomain in parsed_results.subdomains]
        ip_mappings = [{"scan_id": scan_id, "ip": ip} for ip in parsed_results.ips]
        email_mappings = [{"scan_id": scan_id, "email": email} for email in parsed_results.emails]

        db.bulk_insert_mappings(SubdomainModel, subdomain_mappings)
        db.bulk_insert_mappings(IPModel, ip_mappings)
        db.bulk_insert_mappings(EmailModel, email_mappings)

        db.commit()

        return ScanStatus(
            id=scan_id,
            type=scan_request.scan_type,
            website=scan_request.website,
            status="Completed",
            results=parsed_results,
            created_at=start_time,
            completed_at=datetime.now()
        )
    
    except Exception as e:
        logging.exception(f"Error running scan: {e}")
        return ScanStatus(
            id=scan_id,
            type=scan_request.scan_type,
            website=scan_request.website,
            status="Failed",
            results=parsed_results,
            created_at=start_time,
            completed_at=datetime.now()
        )

async def get_results(scan_id: str, db: Session):
    scan_result = db.query(ScanResultModel).options(
        joinedload(ScanResultModel.ips),
        joinedload(ScanResultModel.subdomains),
        joinedload(ScanResultModel.emails)
    ).filter(ScanResultModel.id == scan_id).first()

    if not scan_result:
        raise HTTPException(status_code=404, detail="Scan not found")

    return ScanResultWithIPs(
        id=scan_result.id,
        scan_type=scan_result.scan_type,
        website=scan_result.website,
        status=scan_result.status,
        target=scan_result.target,
        created_at=scan_result.created_at,
        completed_at=scan_result.completed_at,
        ips=[ip.ip for ip in scan_result.ips],
        subdomains=[subdomain.subdomain for subdomain in scan_result.subdomains],
        emails=[email.email for email in scan_result.emails],
        error=scan_result.error
    )