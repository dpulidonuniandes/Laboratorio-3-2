import struct
import hashlib
import os 
def hash_file(filename):
    
    md5_hash = hashlib.md5()
    with open(filename,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
    print("TaMAño \n")
    print(os.path.getsize(filename))
    return md5_hash.hexdigest()

print(hash_file("cliente1.txt"))


