import requests
from urllib.parse import urljoin
COMMON_MISCONFIG_PATHS = [
    "/admin",
    "/admin.php",
    "/admin/login",
    "/adminpanel",
    "/administrator",
    "/backup",
    "/backup.zip",
    "/backups",
    "/config",
    "/config.php",
    "/configuration.php",
    "/debug",
    "/debug.php",
    "/dev",
    "/env",
    "/error",
    "/install",
    "/install.php",
    "/login",
    "/old",
    "/panel",
    "/phpinfo.php",
    "/private",
    "/server-status",  # Apache mod_status
    "/settings",
    "/setup",
    "/staging",
    "/storage",
    "/support",
    "/temp",
    "/test",
    "/test.php",
    "/tmp",
    "/upload",
    "/uploads",
    "/webadmin",
    "/webconfig",
    "/wp-admin",
    "/wp-login.php",
    "/.env",
    "/.git/",
    "/.git/config",
    "/.svn/",
    "/.DS_Store",
    "/crossdomain.xml",
    "/robots.txt",
    "/sitemap.xml"
]


def path_fuzzer(url: str):
    raport = {}
    print(f"[+] Looking for misconfigured or sensitive paths on {url}")
    for path in COMMON_MISCONFIG_PATHS:
        new_url = urljoin(url, path)
        try:
            res = requests.get(new_url)
        except Exception as e:
            print(f"[!] An erros has occured: {e}")
        if res.status_code == 200:
            raport[f"{url}/{path}"] = {
                        "message": "Potential security misconfiguration detected",
                        "path": path
                    }
    return raport