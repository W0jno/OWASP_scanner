import socket
"""     445,   # Microsoft-DS
    465,   # SMTPS
    587,   # SMTP (submission)
    993,   # IMAPS
    995,   # POP3S
    1433,  # MSSQL
    1521,  # Oracle DB
    1723,  # PPTP
    2049,  # NFS
    2082,  # cPanel
    2083,  # cPanel SSL
    3306,  # MySQL
    3389,  # RDP
    5432,  # PostgreSQL
    5900,  # VNC
    6379,  # Redis
    8000,  # Alternatywny HTTP
    8008,  # HTTP (proxy)
    8080,  # HTTP alternatywny
    8081,  # Admin interface
    8443,  # HTTPS alternatywny
    8888,  # HTTP/dev UI
    9200,  # Elasticsearch
    10000, # Webmin
    27017  # MongoDB """
COMMON_PORTS = [
    21,    # FTP
    22,    # SSH
    23,    # Telnet
    25,    # SMTP
    53,    # DNS
    80,    # HTTP
    110,   # POP3
    111,   # RPCBind
    135,   # Microsoft RPC
    139,   # NetBIOS
    143,   # IMAP
    161,   # SNMP
    443   # HTTPS
]
def port_scanner(url: str):
    print(f"[+] Looking for open ports on {url}")
    raport = {}
    try:
        ip = socket.gethostbyname(url.replace("http://", "").replace("https://", "").split("/")[0])
    except socket.gaierror:
        return {"error": f"Could not resolve hostname: {url}"}
    for port in COMMON_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        res = sock.connect_ex((ip, port))
        if res == 0:
            raport[f"{url}:{port}"] = {
                        "message": "Port is open",
                        "port": port  
                    }
        sock.close()
    return raport