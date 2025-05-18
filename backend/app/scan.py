from app.scans.https_checker import check_https
from app.scans.headers_checker import check_headers
from db import models
from db import schemas

def start_scan(url: str, db):
    print(f"Starting scan for {url}")
    vulnerabilities = []
    if not check_https(url):
       vulnerabilities.append(
           schemas.VulnerabilityCreate(
               scan_id=db.id,
               vulnerability_type="HTTPS",
               description="The site does not use HTTPS",
               severity="High"
           )
       )
    check_headers_raport = check_headers(url)

    for header, value in check_headers_raport.items():
        if value == "Missing":
            vulnerabilities.append(
                schemas.VulnerabilityCreate(
                    scan_id=db.id,
                    vulnerability_type="Cryptographic Failures",
                    description=f"The {header} header is missing",
                    severity="Medium"
                )
            )
            continue
        vulnerabilities.append(
                schemas.VulnerabilityCreate(
                    scan_id=db.id,
                    vulnerability_type="Cryptographic Failures",
                    description=f"The {header} header has incorrect value",
                    severity="Medium"
                )
            )
        
    return vulnerabilities
