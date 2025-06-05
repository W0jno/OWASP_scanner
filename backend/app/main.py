from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.database import SessionLocal, engine
from db import models
from db import schemas
from app.scan import start_scan


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "dupa"}

"""
SCANS ENDPOINTS
"""

@app.delete("/scans/all", response_model=schemas.ScanOut)
def delete_scans(db: Session = Depends(get_db)):
    db.query(models.Scan).delete()
    db.commit()
    db.execute(text("ALTER SEQUENCE scans_id_seq RESTART WITH 1;"))
    db.commit()
    return {"message": "All scans deleted"}


@app.post("/scans/start", response_model=schemas.ScanOut)
def create_scan(
    scan: schemas.ScanCreate,
    db: Session = Depends(get_db)
):
    site_to_scan = scan.url.lower()

    # Check if the site is already scanned
    db_scan = models.Scan(**scan.dict())
    db.add(db_scan)
    db.flush()
    vulns = start_scan(site_to_scan, db_scan)

    # Save vulnerabilities and build result summary
    result_lines = []
    for vuln in vulns:
        db_vuln = models.Vulnerability(**vuln.dict())
        db.add(db_vuln)
        db.commit()
        db.refresh(db_vuln)
        result_lines.append(
            f"- [{db_vuln.severity.upper()}] {db_vuln.vulnerability_type}: {db_vuln.description}"
        )

    # Update scan result field
    db_scan.result = "\n".join(result_lines)
    db.commit()
    db.refresh(db_scan)
    return db_scan

@app.get("/scans/all", response_model=list[schemas.ScanOut])
def read_scans(db: Session = Depends(get_db)):
    scans = db.query(models.Scan).all()
    return scans

@app.get("/scans/{id}", response_model=schemas.ScanOut)
def read_scan(id: int, db: Session = Depends(get_db)):
    scan = db.query(models.Scan).filter(models.Scan.id == id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan


"""
VULNERABILITIES ENDPOINTS
"""

@app.get("/vulnerabilities/all", response_model=list[schemas.VulnerabilityOut])
def read_vulnerabilities(db: Session = Depends(get_db)):
    vulnerabilities = db.query(models.Vulnerability).all()
    return vulnerabilities



@app.delete("/vulnerabilities/all", response_model=schemas.VulnerabilityOut)
def delete_vulnerabilities(db: Session = Depends(get_db)):
    db.query(models.Vulnerability).delete()
    db.commit()
    db.execute(text("ALTER SEQUENCE vulnerabilities_id_seq RESTART WITH 1;"))
    db.commit()
    return {"message": "All vulnerabilities deleted"}
