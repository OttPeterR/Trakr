import hashlib

def hash(obj):
    return hashlib.sha256(str(obj)).hexdigest()

def getHashString(obj):
    return str(int(hash(obj), 16))