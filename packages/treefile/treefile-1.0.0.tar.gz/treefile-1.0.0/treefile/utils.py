import hashlib
from pathlib import Path


def compute_checksum(file_path):
    """
    Compute the MD5 checksum of the given file.
    """
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def cache_checksum(treefile_path, checksum):
    """
    Cache the checksum in a companion file.
    """
    cache_path = Path(str(treefile_path) + ".cache")
    with open(cache_path, "w") as f:
        f.write(checksum)


def get_cached_checksum(treefile_path):
    """
    Retrieve the cached checksum, if it exists.
    """
    cache_path = Path(str(treefile_path) + ".cache")
    if cache_path.exists():
        with open(cache_path, "r") as f:
            return f.read().strip()
    return None


def should_reprocess(treefile_path):
    """
    Compare the current checksum with the cached checksum to decide if processing is needed.
    If the file has changed, update the cache and return True.
    """
    current_checksum = compute_checksum(treefile_path)
    cached = get_cached_checksum(treefile_path)
    if cached != current_checksum:
        cache_checksum(treefile_path, current_checksum)
        return True
    return False
