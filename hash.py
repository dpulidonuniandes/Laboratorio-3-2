import struct
import hashlib
import os 
def hash_file(filename):
    
    md5_hash = hashlib.md5()
    with open(filename,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)

    return md5_hash.hexdigest()





