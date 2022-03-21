import ecdsa
import json
import base58
class account:
    def __init__(self):
        self.sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST521p)
        self.PrivateKey =  base58.b58encode(self.sk.to_string())
        self.PublicKey = base58.b58encode(self.sk.verifying_key.to_string("uncompressed"))
    def signTransaction(self,message):
        sig = self.sk.sign(message)
        if self.sk.verifying_key.verify(sig,message):
            return base58.b58encode(sig)
        else:
            return False
    def verfyTransaction(self,sig,message):
        return self.sk.verifying_key.verify(base58.b58decode(sig),message)

transac = {"sender": "A", "receiver": "B", "amount": 100, "timestamp": 1647690547.3355699}

a = account()
print(a.PrivateKey)
print("-"*10)
print(a.PublicKey)
message = bytes(json.dumps(transac),'utf-8')
print("-"*10)
sig = a.signTransaction(message)

print(sig)

print("-"*10)
print(a.verfyTransaction(sig,message))



