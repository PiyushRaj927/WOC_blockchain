#import all
from tempfile import tempdir
import blockchain
import mongo
import server
import threading
things_to_execute = []
things_executing = []
cmd_list = {}
#init all things
ledger_db = mongo.ledger()
update_db = mongo.update()
nodes_db = mongo.nodes()
ledger = blockchain.Blockchain([ledger_db,update_db,nodes_db])


def watcher():
    while True:
        if things_to_execute:
            temp_cmd = things_to_execute.pop(0)
            things_executing.append(temp_cmd)
            fn = cmd_list.get(temp_cmd)
            threading.Thread(target=fn).start()


port = 5020
name = "server1"
connected_nodes = nodes_db
node = server.GossipNode(port,connected_nodes,name)
node.start_threads()

threading.Thread(target=watcher).start()
ledger.add_new_transaction()







