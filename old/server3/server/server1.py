import importlib.machinery
import importlib.util
import time
import json
# import the GossipNode class
Gossip_loader = importlib.machinery.SourceFileLoader( 'Gossip', './Gossip.py' )
Gossip_spec = importlib.util.spec_from_loader( 'Gossip',Gossip_loader )
Gossip = importlib.util.module_from_spec(Gossip_spec)
Gossip_spec.loader.exec_module(Gossip)


# port for this node
port = 5020
# ports for the nodes connected to this node
connected_nodes = [5000]
name = 'server2'
server = Gossip.GossipNode(port, connected_nodes,name)


