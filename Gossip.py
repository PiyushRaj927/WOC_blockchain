import random
import socket
from threading import Thread
import time
import json

import importlib.machinery
import importlib.util
#import main
"""# Import node
node_loader = importlib.machinery.SourceFileLoader( 'node', './node1/server1.py' )
node_spec = importlib.util.spec_from_loader( 'node', node_loader )
node = importlib.util.module_from_spec(node_spec)
node_spec.loader.exec_module(node)"""

votes=[]
cmd = []

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
        


        print("Node started on port {0}".format(self.port))
        print("Susceptible nodes =>", self.susceptible_nodes)

        self.start_threads()

    def input_message(self):
        while True:
            message_to_send = input("Enter a message to send:\n")

            self.transmit_message(message_to_send.encode('ascii'))

    def receive_message(self):
            while True:
                self.node.listen()
                conn, address= self.node.accept()
                message_to_forward = conn.recv(1024)
                conn.close()
                if self.susceptible_nodes != []:
                     
                    self.susceptible_nodes.remove(address[1]-1)
                    GossipNode.infected_nodes.append(address[1])
                if message_to_forward:
                    time.sleep(2)

                    
                    print("\nMessage is: '{0}'.\nReceived at [{1}] from [{2}]\n"
                            .format(message_to_forward.decode('ascii'), time.ctime(time.time()), address[1]))
                data =json.loads(message_to_forward.decode('ascii'))
                cmd.append(data)
                print("cmd:\n",cmd)
                   #self.transmit_message(vote_data.encode('ascii'))

    def transmit_message(self, message):
        
        for selected_port in self.known_nodes:
            #selected_port = random.choice(self.susceptible_nodes)

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
            self.node2.sendall(message)
            self.node2.close()
            
            
            """self.susceptible_nodes.remove(selected_port)
            GossipNode.infected_nodes.append(selected_port)"""

            print("Message: '{0}' sent to [{1}].".format(message.decode('ascii'), selected_port))
            """print("Susceptible nodes =>", self.susceptible_nodes)
            print("Infected nodes =>", GossipNode.infected_nodes)"""
            print("-"*50)
            time.sleep(1)
            print("\ndone")

    def start_threads(self):
      
        #Thread(target=self.input_message).start()
        Thread(target=self.receive_message).start()
"""    def decode_message(self,message):
        text = message.decode('ascii')
        decoded = json.load(text)
        return decoded
    def encode_message(self,message):"""
        
