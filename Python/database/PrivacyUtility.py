import hashlib

def hash(obj):
    return hashlib.sha256(str(obj)).hexdigest()