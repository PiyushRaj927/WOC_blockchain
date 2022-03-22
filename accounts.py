import ecdsa
import json
import base58
class account:
    def __init__(self):
        self.sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST521p)
        self.PrivateKey =  base58.b58encode(self.sk.to_pem())
        
        self.PublicKey = base58.b58encode(self.sk.verifying_key.to_pem())
        print("\nPrivateKey","\n",self.PrivateKey,"\n")
        self.vk = ecdsa.VerifyingKey.from_pem(base58.b58decode(self.PublicKey))
        del self.PrivateKey
        del self.sk
    def signTransaction(self,message):
        Privatekey = ecdsa.SigningKey.from_pem(base58.b58decode(input("Enter your Privatekey:\n")))
        sig = Privatekey.sign(message)
        if self.vk.verify(sig,message):
            return base58.b58encode(sig)
        else:
            print("[*] error signed transaction can't be verified ")
            return 
    def verfyTransaction(self,sig,message):
        return self.vk.verify(base58.b58decode(sig),message)

transac = {"sender": "A", "receiver": "B", "amount": 100, "timestamp": 1647690547.3355699}

a = account()
print("-"*10)
print(a.PublicKey)
message = bytes(json.dumps(transac),'utf-8')
print("-"*10)
sig = a.signTransaction(message)

print(sig)

print("-"*10)
print(a.verfyTransaction(sig,message))



