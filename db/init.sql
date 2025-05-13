
CREATE TABLE IF NOT EXISTS scans (
    id SERIAL PRIMARY KEY,
    target_url TEXT NOT NULL,
    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vulnerabilities JSONB
);
