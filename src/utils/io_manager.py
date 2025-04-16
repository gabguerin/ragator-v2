import hashlib


def hash_value(obj) -> str:
    """Generate a hash from a Python object (usually a list of URLs or file paths)."""
    m = hashlib.sha256()
    if isinstance(obj, (list, tuple)):
        for item in obj:
            m.update(str(item).encode())
    else:
        m.update(str(obj).encode())
    return m.hexdigest()
