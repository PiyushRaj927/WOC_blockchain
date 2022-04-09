import random
import socket
from threading import Thread
import time
import os
import json
from Crypto.Hash import SHA256
import importlib.machinery
import importlib.util

import ecdsa
import json
from Crypto.Hash import keccak
import base58


votes=[]
cmd = []

class server_accounts:
    def __init__(self,name):
        if os.path.exists("{}--private.pem".format(name)) and os.path.exists("{}--public.pem".format(name)):
            with open("{}--private.pem".format(name), "rb+") as f:
                self.sk = ecdsa.SigningKey.from_pem(f.read())

            with open("{}--public.pem".format(name), "a+") as f:
                #self.vk = self.sk.verifying_key.from_pem(f.read())
                pass
        else:
            self.sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST521p)
            with open("{}--private.pem".format(name), "wb") as f:
                f.write(self.sk.to_pem())
            with open("{}--public.pem".format(name), "wb") as f:
                f.write(self.sk.verifying_key.to_pem())
        self.PrivateKey =  base58.b58encode(self.sk.to_pem())
            
        self.PublicKey = base58.b58encode(self.sk.verifying_key.to_pem())
            
        self.vk = ecdsa.VerifyingKey.from_pem(base58.b58decode(self.PublicKey))
        pub_hash = keccak.new(digest_bits=256)
        pub_hash.update(self.PublicKey)
        self.Addr = pub_hash.hexdigest()
                
        
    def signTransaction(self,message):
        Privatekey = ecdsa.SigningKey.from_pem(base58.b58decode(self.PrivateKey))
        sig = Privatekey.sign(message)
        if self.vk.verify(sig,message):
            return base58.b58encode(sig)
        else:
            print("[*] error signed transaction can't be verified ")
            return False
    def verfyTransaction(self,sig,message):
        return self.vk.verify(base58.b58decode(sig),message)


class GossipNode:
    infected_nodes = []

    def __init__(self, port, connected_nodes,name):
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.known_nodes = connected_nodes
        self.hostname = 'localhost'
        self.susceptible_nodes = connected_nodes
        self.port = port
        self.name = name
        self.node.bind((self.hostname, self.port))
        self.identity = server_accounts(name)

        print("Node started on port {0}".format(self.port))
        print("Susceptible nodes =>", self.susceptible_nodes)

        self.start_threads()
    def verify_messsage(self,id,sig,message):
        vk = ecdsa.VerifyingKey.from_pem(base58.b58decode(id))
        return vk.verify(base58.b58decode(sig),message)
    def create_id(self,message):
        h = SHA256.new()
        h.update(bytes(message,'utf-8'))
        return h


    def input_message(self):
        while True:
            message_to_send = input("Enter a message to send:\n")

            self.transmit_message(message_to_send.encode('utf-8'))

    def receive_message(self):
            while True:
                self.node.listen()
                conn, address= self.node.accept()
                message_to_forward = bytearray()
                while True:
                    data = conn.recv(1024)
                    message_to_forward += data
                    if not data:
                        break

                #message_to_forward = conn.recv(1024)
                conn.close()
                if message_to_forward:
                    print(message_to_forward.decode('utf-8'))
                """if self.susceptible_nodes != []:
                     
                    self.susceptible_nodes.remove(address[1]-1)
                    GossipNode.infected_nodes.append(address[1])"""
                if message_to_forward:
                    print(message_to_forward.decode('utf-8'))
                    message = json.loads(message_to_forward.decode('utf-8'))
                    if self.verify_messsage(bytes(message['id'],'utf-8'),bytes(message['sig'],'utf-8'),bytes(json.dumps(message['data']),'utf-8')):

                        print("\nMessage is: '{0}'.\nReceived at [{1}] from [{2}]\n"
                            .format(message, time.ctime(time.time()), address[1]))
                            #data =json.loads(message_to_forward.decode('utf-8'))
                        
                        
                        cmd.append(message['data'])
                        print("cmd:\n",cmd)
                        #self.transmit_message(vote_data.encode('utf-8'))

    def transmit_message(self, message):
        
        for selected_port in self.known_nodes:
            #selected_port = random.choice(self.susceptible_nodes)
            message_sig = self.identity.signTransaction(bytes(json.dumps(message),'utf-8')).decode('utf-8')
            print(message_sig)
            message_to_forward = json.dumps({'update_id':self.create_id(message),'data':message,'sig':message_sig,'id':self.identity.PublicKey.decode('utf-8')}).encode("utf-8")
            print(message_to_forward)
            """ print("\n")
            print("-"*50)
            print("Susceptible nodes =>", self.susceptible_nodes)
            print("Infected nodes =>", GossipNode.infected_nodes)
            print("Port selected is [{0}]".format(selected_port))"""

            print("---------",selected_port)        
            self.node2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.node2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.node2.bind(('localhost',self.port+1))
            self.node2.connect(('localhost', selected_port))
            self.node2.sendall(message_to_forward)
            self.node2.close()
            
            
            """self.susceptible_nodes.remove(selected_port)
            GossipNode.infected_nodes.append(selected_port)"""

            #print("Message: '{0}' sent to [{1}].".format(json.dumps(message_to_forward), selected_port))
            """print("Susceptible nodes =>", self.susceptible_nodes)
            print("Infected nodes =>", GossipNode.infected_nodes)"""
            print("-"*50)
            time.sleep(1)
            print("\ndone")

    def start_threads(self):
      
        #Thread(target=self.input_message).start()
        Thread(target=self.receive_message).start()
"""    def decode_message(self,message):
        text = message.decode('utf-8')
        decoded = json.load(text)
        return decoded
    def encode_message(self,message):"""
        
