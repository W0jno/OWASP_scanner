import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
sqli_payloads = [
    "'",
    "''",
    "`",
    "``",
    ",",
    ";",
    "-- or #",
    "' OR '1",
    "'='",
    "'LIKE'"
]
xss_payloads = [
    '"><svg/onload=alert(1)>',
    '\'><svg/onload=alert(1)>',
    '<img src=x onerror=alert(1)>',
    '"><img src=x onerror=alert(1)>',
    '\'><img src=x onerror=alert(1)>',
    "';alert(String.fromCharCode(88,83,83))//';alert(String.fromCharCode(88,83,83))//--></script>",
    "<Script>alert('XSS')</scripT>",
    "<script>alert(document.cookie)</script>",
]
sql_errors = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "mysql_fetch",
    "syntax error",
    "odbc",
    "sql error",
    "native client",
    "pg_query",
    "mysql_num_rows",
    "ORA-01756",
    "Microsoft OLE DB Provider for SQL Server"
]
def scan_sqli_params(url):
    raport = {}
    """
    Scanning website for sqli injection
    """
    print(f"[+] Testing SQLi on {url}")

    for payload in sqli_payloads:
        try:
            params = {id: payload}
            res= requests.get(url, params=params, timeout=5)
            if is_sql_error(res.text) or res.status_code == 500:
                raport[payload] = "SQL injection in parameter"
                break;
        except Exception as e:
            print(f"[!] An error has occurred with payload: {e}")
    return raport

def scan_sqli_forms(url):
    """
    Scanning website for sqli injection
    """
    
    raport = {}
    data = {}
    forms = get_all_forms(url)
    forms_details = [get_form_detail(form) for form in forms]
    for form in forms_details:
        for payload in sqli_payloads:
            for input_tag in form["inputs"]:
                key = input_tag["value"]
                value = input_tag["name"]
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    try:
                        data[key] = value + payload
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    data[key] = f"test{payload}"
            url = urljoin(url, form["action"])
            if form["method"] == "post":
                res = requests.post(url, data=data)
            elif form["method"] == "get":
                res = requests.get(url, params=data)
            try:
                if is_sql_error(res.text) or res.status_code == 500:
                    raport[f"form:{payload}"] = {
                        "message": "SQL injection in form",
                        "form": form  # Pass the form details
                    }
            except Exception as e:
                print(f"[!] An error has occurred with payload: {e}")

    remove_duplicate_inputs(raport)
    return raport

def scan_xss(url):
    """
    Scanning website for XSS injection
    """
    print(f"[+] Testing XSS on {url}")
    raport = {}
    data = {}
    forms = get_all_forms(url)
    forms_details = [get_form_detail(form) for form in forms]
    for form in forms_details:
        for payload in xss_payloads:
            for input_tag in form["inputs"]:
                name = input_tag.get("name")
                if not name:
                    continue  # field without "name" won't be send
                if input_tag["type"] == "hidden" or input_tag.get("value"):
                    data[name] = input_tag.get("value", "") + payload
                elif input_tag["type"] != "submit":
                    data[name] = f"test{payload}"
            url = urljoin(url, form["action"])
            if form["method"] == "post":
                res = requests.post(url, data=data)
            elif form["method"] == "get":
                res = requests.get(url, params=data)
            try:
                if res and payload in res.content.decode():
                    raport[f"form:{payload}"] = {
                        "message": "XSS injection in form",
                        "form": form
                    }
            except Exception as e:
                print(f"[!] An error has occurred with payload: {e}")

    remove_duplicate_inputs(raport)
    return raport

def remove_duplicate_inputs(raport):
    unique_inputs = set()
    filtered_raport = {}
    for k, v in raport.items():
        if isinstance(v, dict) and "form" in v:
            # Use a tuple of action and sorted input names as a unique form key
            form = v["form"]
            form_key = (form["action"], tuple(sorted(inp["name"] for inp in form["inputs"] if inp["name"])))
            if form_key not in unique_inputs:
                unique_inputs.add(form_key)
                filtered_raport[k] = v
        else:
            filtered_raport[k] = v  # Keep non-form entries as is
    raport.clear()
    raport.update(filtered_raport)

def get_all_forms(url):
    """
    Return all forms from the HTML content
    """
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_detail(form):
    """
    Extracts all possible useful information about HTML form
    """
    action = form.attrs.get("action")
    action = action.lower() if action else None
    method = form.attrs.get("method", "get").lower()

    inputs = [
        {
            "type": input_tag.attrs.get("type", "text"),
            "name": input_tag.attrs.get("name"),
            "value": input_tag.attrs.get("value", "")
        }
        for input_tag in form.find_all("input")
    ]
    return {
        "action": action,
        "method": method,
        "inputs": inputs
    }

def is_sql_error(response_text):
    text = response_text.lower()
    return any(err in text for err in sql_errors)