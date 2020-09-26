import hashlib


def is_url(query_parsed):
    if query_parsed.scheme and query_parsed.netloc and query_parsed.path:
        return True
    return False


def generate_hash(value: str):
    value = str(value)
    hashed = hashlib.md5(value.encode())
    return str(hashed.hexdigest())
