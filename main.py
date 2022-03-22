import importlib.machinery
import importlib.util
from pathlib import Path

#Import accounts
accounts_loader = importlib.machinery.SourceFileLoader( 'accounts', './accounts.py' )
accounts_spec = importlib.util.spec_from_loader( 'accounts', accounts_loader )
accounts = importlib.util.module_from_spec( accounts_spec )
accounts_spec.loader.exec_module(accounts)

# Import blockchain
blockchain_loader = importlib.machinery.SourceFileLoader( 'blockchain', './blockchain/blockchain.py' )
blockchain_spec = importlib.util.spec_from_loader( 'blockchain', blockchain_loader )
blockchain = importlib.util.module_from_spec(blockchain_spec)
blockchain_spec.loader.exec_module(blockchain)

ledger = blockchain.Blockchain()
a = accounts.account()
b = accounts.account()
c = accounts.account()

ledger.add_new_transaction(blockchain.Transaction("A","B",100,a.signTransaction(bytes("{'sender': 'A', 'receiver': 'B', 'amount': 100}","utf-8"))))
ledger.mine()



ledger.add_new_transaction(blockchain.Transaction("A","B",200,a.signTransaction(bytes("{'sender': 'A', 'receiver': 'B', 'amount': 200}","utf-8"))))
ledger.mine()