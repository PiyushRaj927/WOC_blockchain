import time
import json
import hashlib

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash ,nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def block_string(self):
        temp = {'index':self.index,
                'transactions':self.transactions,
                'timestamp':self.timestamp,
                'previous_hash': self.previous_hash,
                'nonce':self.nonce}
        return json.dumps(temp)
    def __repr__(self):
        return self.block_string()

    def block_hash(self):
        return hashlib.sha256(self.block_string().encode()).hexdigest()
        
        
        

class Blockchain: 
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
    def len(self):
        return len(self.chain)
    def create_genesis_block(self):
        genesis_block = Block(0, {}, time.time(), "{0:#0{1}x}".format(0,32))
        genesis_block.hash = genesis_block.block_hash()
        self.chain.append(genesis_block)
    def last_block(self):
        return self.chain[-1]
    
    difficulty = 4
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
            transaction.update({'timestamp': time.time()})
            self.unconfirmed_transactions.append(transaction)

    def mine(self):
            if not self.unconfirmed_transactions:
                return False
     
            last_block = self.last_block()
            
            k=last_block.index + 1
            
            new_block = Block(index=last_block.index + 1,
                              transactions=self.unconfirmed_transactions,
                              timestamp=time.time(),
                              previous_hash=last_block.block_hash())
     
            self.proof_of_work(new_block)
            self.add_block(new_block)
            self.unconfirmed_transactions = []
            temp = "Newblock added " + str(new_block.index)
            return temp
    def __repr__(self):
        temp = "length:" + str(self.len()) + "\n" + str(self.chain)
        return temp

blockchain = Blockchain()
blockchain.add_new_transaction({"bob to alice":20})
blockchain.mine()
blockchain.add_new_transaction({"Q to Z":20})
blockchain.add_new_transaction({"A to D":20})
blockchain.add_new_transaction({"V to G":20})
blockchain.mine()