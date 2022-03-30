from operator import attrgetter
from pickle import FALSE
import accounts
import time
import json 
import importlib.machinery
import importlib.util
import base58
import hashlib
from threading import Thread
# Import node
node_loader = importlib.machinery.SourceFileLoader( 'node', './node1/server1.py' )
node_spec = importlib.util.spec_from_loader( 'node', node_loader )
node = importlib.util.module_from_spec(node_spec)
node_spec.loader.exec_module(node)

class Transactions:
    def __init__(self,transaction):
        self.chain = sorted(transaction,key=attrgetter('timestamp'))

    def GET_Balance(self,addr,balance):
    
        for i in self.chain:
            if addr in i.sender :
                balance -= i.amount
            if addr in i.receiver :
                balance += i.amount
        return balance
    def __repr__(self):
        return json.dumps(self.chain)
    def Json(self):
        chain = []
        for i in self.chain:
            chain.append(i.tx)
        return chain 

            
     
class Transaction:
    def __init__(self,sender,receiver,amount,sig):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time() 
        self.sig = sig
        
        self.tx = {"tx":{"sender":self.sender,
                                "receiver":self.receiver,
                                "amount":self.amount},
                                "timestamp":self.timestamp,
                                "sig":base58.b58encode(self.sig).decode()}
    
        self.JSON = json.dumps(self.tx)
        print(self.tx["tx"])
    """  def verify_transaction(self):
        addr = bytes.fromhex(self.sender)
        #get the public key from the database
        ecdsa.VerifyingKey.from_pem(base58.b58decode(self.PublicKey)).verify(base58.b58decode(sig),message)"""
    def __repr__(self):
        return self.JSON
   
        

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash ,nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        

    def block_string(self):
        temp = {'index':self.index,
                'transactions':self.transactions.Json(),
                'timestamp':self.timestamp,
                'previous_hash': self.previous_hash,
                'nonce':self.nonce}
       
        return json.dumps(temp)
    def __repr__(self):
        return self.block_string()

    def block_hash(self):
        return hashlib.sha256(self.block_string().encode()).hexdigest()
    def GET_Balance(self,addr,balance):
        return self.transactions.GET_Balance(addr,balance)
        
        
        
        

class Blockchain: 
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.unconfirmed_block = []
        self.votes = []
        self.create_genesis_block()
        Thread(target=self.temp).start()
    def len(self):
        return len(self.chain)
    def create_genesis_block(self):
        genesis_block = Block(0, Transactions([Transaction("ROOT","A",1000,b'0')]), time.time(), "{0:#0{1}x}".format(0,32))
        genesis_block.hash = genesis_block.block_hash()
        self.chain.append(genesis_block)
    def last_block(self):
        return self.chain[-1]
    
    difficulty = 2
    def proof_of_work(self, block):
            
            computed_hash = block.block_hash()
           
            while not computed_hash.startswith('0' * Blockchain.difficulty):
                block.nonce += 1
                computed_hash = block.block_hash()
               
            
            return 0
    def add_block(self, block):
        previous_hash = self.last_block().block_hash()
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid(block):
            return False
        
        self.chain.append(block)
        
        return True
 
    def is_valid(self, block):
            return block.block_hash().startswith('0' * Blockchain.difficulty)
                    

    def add_new_transaction(self, transaction):
            self.unconfirmed_transactions.append(transaction)
    

    def mine(self,local=True):
            for i in self.unconfirmed_transactions:
               if not self.validate_transactions(i):
                   self.unconfirmed_transactions.remove(i)   
            if not self.unconfirmed_transactions:
                return False
     
            last_block = self.last_block()
            
            k=last_block.index + 1

            new_block = Block(index=last_block.index + 1,
                              transactions=Transactions(self.unconfirmed_transactions),
                              timestamp=time.time(),
                              previous_hash=last_block.block_hash())
     
            self.proof_of_work(new_block)
            if  local:
                self.unconfirmed_block.append(new_block)
                if not self.get_vote(new_block):
                    print("block rejected by network")
                    return False
            self.add_block(new_block)
                    
            self.unconfirmed_transactions.clear()
            
            self.unconfirmed_block.clear()
            temp = "Newblock added " + str(new_block.index)
            return temp
    def __repr__(self):
        temp = "length:" + str(self.len()) + "\n" + str(self.chain)
        return temp
    def validate_transactions(self,transaction):
           
            if self.Get_Balance(transaction.sender) - transaction.amount >= 0:
                return True
            else:
                print("NOt enogh balance")
                return False
    def Get_Balance(self,addr):
        balance = 0
        for i in self.chain:
            
            balance = i.GET_Balance(addr,balance)
        return balance
    def get_vote(self,unconf_block):
        
        vote = self.send_block(unconf_block)
        if vote>=2:
            return True
    def block_verification_network(self,message):
        block = message['data']
        new_block = Block(block['index'],Transactions([Transaction(i["tx"]["sender"],i["tx"]["receiver"],i["tx"]["amount"],i["sig"]) for i in block['transactions']]),block['timestamp'],block['previous_hash'],block['nonce'])
        #if  (new_block.block_hash().startswith('0' * Blockchain.difficulty) and new_block.previous_hash==self.last_block.block_hash()):
        if True:
            print("checking transactions")
            for i in new_block.transactions.chain:
                print(i)
                if  self.validate_transactions(i):
                    self.add_block(new_block)
                    print("block verification done")
                    return True

    def send_block(self,block):
        data = block.block_string()
        message = json.dumps({ 'timestamp': time.time(),
                    'id':node.name,
                    'data':json.loads(data),
                    'type':'block_verification'
                    #'sig':
                        })
        node.server.transmit_message(message.encode('ascii'))      
        while True:
            if len(self.votes)>=2:
                nf_votes =0
                for i in self.votes:
                    if i ==1:
                        nf_votes+=nf_votes
                self.votes = []
                return nf_votes
    def temp(self):
        while True:
            for k in node.Gossip.cmd:
                if k['type']=='block_verification':
                        
                    vote = self.block_verification_network(k)
                    vote_data = json.dumps({ 'timestamp': time.time(),
                                                'data':str(vote),
                                                'id':node.name,
                                                'type':'block_vote'
                    #'sig':
                        })
                    print("sending vote: ",vote_data)
                    node.server.transmit_message(vote_data.encode('ascii'))
                    del k

                """elif k['type']=='block_vote':
                    if k['data'] == 'True':
                        self.votes.append(1)"""   
                    
            


