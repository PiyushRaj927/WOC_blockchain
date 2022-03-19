from Crypto.PublicKey import ECC
from Crypto.Hash import keccak
key = ECC.generate(curve='P-256')
"""f = open('myprivatekey.pem','wt')
f.write(key.export_key(format='OpenSSH'))
f.close()
f = open('myprivatekey.pem','rt')
key = ECC.import_key(f.read())
print(key)
"""
class account:
    def __init__(self):
        self.PrivateKey,self.PublicKey,self.Address = self.gen_key()
        #self.
    def gen_key(self):
        temp = ECC.generate(curve='P-256')
        private_key = (temp.export_key(passphrase="hi",format='DER',protection='PBKDF2WithHMAC-SHA1AndAES128-CBC').hex())
        public_key = temp.public_key().export_key(format='DER').hex()
        k = keccak.new(digest_bits=256)
        k.update(bytes.fromhex(public_key))
        Address = k.hexdigest()
        
        return ('0x'+private_key),('0x'+public_key),('0x'+Address)
        







