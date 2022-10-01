
import hashlib
 
def hash_file():
    filename = None
    tipo =int(input("Escriba el numero del archivo que usara \n 1- 100MB \n 2- 250MB \n"))
    if (tipo==1):
        filename = "archivo1.txt"
    else:
        filename = "archivo2.txt"

    md5_hash = hashlib.md5()
    with open(filename,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
    print(md5_hash.hexdigest())
    return

