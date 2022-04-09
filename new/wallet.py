import ecdsa
import json
from Crypto.Hash import keccak
import base58
class account:
    def __init__(self):
        self.sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST521p)
        self.PrivateKey =  base58.b58encode(self.sk.to_pem())
        self.PublicKey = base58.b58encode(self.sk.verifying_key.to_pem())
        while True:
            ans = input(""" 
            1) print the key 
            2)encrypted with a passphrase and save to a file
            
            
            """)
        print("\nPrivateKey","\n",self.PrivateKey,"\n")
        self.vk = ecdsa.VerifyingKey.from_pem(base58.b58decode(self.PublicKey))
        pub_hash = keccak.new(digest_bits=256)
        pub_hash.update(self.PublicKey)
        self.Addr = pub_hash.hexdigest()
                
        del self.PrivateKey
        del self.sk
    def signTransaction(self,message):
        Privatekey = ecdsa.SigningKey.from_pem(base58.b58decode(input("Enter your Privatekey:\n")))
        sig = Privatekey.sign(message)
        if self.vk.verify(sig,message):
            return base58.b58encode(sig)
        else:
            print("[*] error signed transaction can't be verified ")
            return False
    def verfyTransaction(self,sig,message):
        return self.vk.verify(base58.b58decode(sig),message)





