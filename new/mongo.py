from pymongo import MongoClient
client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.3.1')
import json
class ledger:
    def __init__(self):
        self.blockchain_ledger_db = client['blockchain_ledger']
        self.blockchain_collection = self.blockchain_ledger_db["ledger_0"]
        self.blockchain_collection.delete_many({})
        self.currentblock_index = 0
        

        
    def insert_one_block(self,block):
        self.blockchain_collection.insert_one(json.loads(block.block_string()))
        self.currentblock_index += 1
        print("block added to mongo")
        return self.currentblock_index
    def insert_many_block(self,block_list):
        for block in block_list:
            self.blockchain_collection.insert_one(block.block_string())
            self.currentblock_index += 1
    def get_block(self,index): 
        return self.blockchain_collection.find_one({'index':index})
    """def delete_block(self,index):
        self.blockchain_collection.delete_one({'index':index})
        pass"""
            
        
        

        
    


class update():
    def __init__(self):
        self.updates_db = client['updates']
        self.update_collection = self.updates_db['update_list']
        self.update_collection.delete_many({})
        pass

class nodes():
    def __init__(self):
        self.node_db = client['node']
        self.node_collection = self.node_db['node_list']
        self.node_collection.delete_many({})
        with open('node_list.json','r') as f:
            init_list = json.load(f)
        for i in init_list["initial_nodelist"]:
            self.node_collection.insert_one(init_list)

        pass
    def get_list(self):
        return self.node_collection.find()
    def add_node():
        pass





















