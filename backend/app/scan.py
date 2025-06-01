from app.scans.https_checker import check_https
from app.scans.headers_checker import check_headers
from app.scans.port_scanner import port_scanner
from app.scans.path_fuzzer import path_fuzzer
from app.scans.injection_scanner import scan_sqli_params, scan_sqli_forms, scan_xss
from db import models
from db import schemas


def start_scan(url: str, db):
    print(f"Starting scan for {url}")
    vulnerabilities = []
    """
    SCANS AND RAPORTS
    """
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
    sqli_params_raport = scan_sqli_params(url)
    sqli_forms_raport = scan_sqli_forms(url)
    xss_forms_raport = scan_xss(url)
    port_raport = port_scanner(url)
    path_fuzzer_raport = path_fuzzer(url);
    combined_raports = combine_all_raports(check_headers_raport, sqli_params_raport, sqli_forms_raport, xss_forms_raport, port_raport, path_fuzzer_raport)
    header_names = {
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Strict-Transport-Security",
    "Referrer-Policy",
    "Permissions-Policy",
    "Access-Control-Allow-Origin"
    }

    for key, value in combined_raports.items():
        if key in header_names:
            if value == "Missing":
                vulnerabilities.append(
                    schemas.VulnerabilityCreate(
                        scan_id=db.id,
                        vulnerability_type="Cryptographic Failures",
                        description=f"The {key} header is missing",
                        severity="Medium"
                    )
                )
            else:
                vulnerabilities.append(
                    schemas.VulnerabilityCreate(
                        scan_id=db.id,
                        vulnerability_type="Cryptographic Failures",
                        description=f"The {key} header has incorrect value",
                        severity="Medium"
                    )
                )
        elif value == "SQL injection in parameter":
            vulnerabilities.append(
                schemas.VulnerabilityCreate(
                    scan_id=db.id,
                    vulnerability_type="SQL injection",
                    description=f"The target URL is vulnerable to SQL injection",
                    severity="High"
                )
            )
        elif isinstance(value, dict) and value.get("message") == "SQL injection in form":
            vulnerabilities.append(
                schemas.VulnerabilityCreate(
                    scan_id=db.id,
                    vulnerability_type="SQL injection",
                    description=f"The target URL is vulnerable to SQL injection in form {value.get('form')}",
                    severity="High"
                )
            )
        elif isinstance(value, dict) and value.get("message") == "XSS injection in form":
            vulnerabilities.append(
                schemas.VulnerabilityCreate(
                    scan_id=db.id,
                    vulnerability_type="XSS injection",
                    description=f"The target URL is vulnerable to XSS injection in form {value.get('form')}",
                    severity="High"
                )
            )
        elif isinstance(value, dict) and value.get("message") == "Port is open":
            vulnerabilities.append(
                schemas.VulnerabilityCreate(
                    scan_id=db.id,
                    vulnerability_type="Open port",
                    description=f"Port {value.get('port')} is open on the target system.",
                    severity="High"
                )
            )
        elif isinstance(value, dict) and value.get("message") == "Potential security misconfiguration detected":
            vulnerabilities.append(
                schemas.VulnerabilityCreate(
                    scan_id=db.id,
                    vulnerability_type="Potential security misconfiguration",
                    description=f"Accessible sensitive path: {value.get('path')}",
                    severity="Medium"
                )
            )
    return vulnerabilities

def combine_all_raports(headers_rap, sqli_params_rap, sqli_forms_rap, xss_forms_rap, port_rap, path_fuzzer_rap):
    combined_raport = {**headers_rap, **sqli_params_rap, **sqli_forms_rap, **xss_forms_rap, **port_rap, **path_fuzzer_rap}
    return combined_raport
