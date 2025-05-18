def check_https(url) -> bool:
    """
    Check if the given URL uses HTTPS.
    """
    if url.startswith("https://"):
        return True
    elif url.startswith("http://"):
        return False
    else:
        raise ValueError("URL must start with http:// or https://")