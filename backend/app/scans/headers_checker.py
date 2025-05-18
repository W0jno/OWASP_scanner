import requests

def check_headers(url):
    """
    Check the HTTP headers of the given URL.
    """
    headers_to_check = ["Content-Security-Policy", "X-Content-Type-Options", "X-Frame-Options", "Strict-Transport-Security", "Referrer-Policy", "Permissions-Policy", "Access-Control-Allow-Origin"]
    raport = {}
    headers = requests.get(url).headers
    for header in headers_to_check:
        if header not in headers:
            raport[header] = "Missing"
    
    for header,value in headers.items():
        match header:
            case "Content-Security-Policy":
                if value != "":
                    continue
            case "X-Content-Type-Options":
                if value != "nosniff":
                    raport[header] = "Incorrect value"
            case "X-Frame-Options":
                if value != "DENY" and value != "SAMEORIGIN":
                    raport[header] = "Incorrect value"
            case "Strict-Transport-Security":
                if value == "" or value !="max-age":
                    raport[header] = "Incorrect value"
            case "Referrer-Policy":
                if value != "no-referrer" and value != "same-origin":
                    raport[header] = "Incorrect value"
            case "Permissions-Policy":
                if value != "geolocation=()":
                    raport[header] = "Incorrect value"
            case "Access-Control-Allow-Origin":
                if value != "*":
                    raport[header] = "Incorrect value"
    return raport
