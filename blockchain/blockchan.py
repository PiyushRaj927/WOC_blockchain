from operator import attrgetter
import accounts
import time
import json
import hashlib
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
            
     
class Transaction:
    def __init__(self,sender=None,receiver=None,amount=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time() 
        temp = {"sender":self.sender,
                                "receiver":self.receiver,
                                "amount":self.amount,
                                "timestamp":self.timestamp}
    
        self.JSON = json.dumps(temp)

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
                'transactions':repr(self.transactions.chain),
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
        self.create_genesis_block()
    def len(self):
        return len(self.chain)
    def create_genesis_block(self):
        genesis_block = Block(0, Transactions([Transaction("ROOT","A",1000)]), time.time(), "{0:#0{1}x}".format(0,32))
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
    

    def mine(self):
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
            self.add_block(new_block)
            self.unconfirmed_transactions.clear()
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
            
            
blockchain = Blockchain()

blockchain.add_new_transaction(Transaction("A","B",100))
blockchain.mine()
blockchain.add_new_transaction(Transaction("A","B",200))
blockchain.mine()