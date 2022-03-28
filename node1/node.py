import importlib.machinery
import importlib.util


# import the GossipNode class
Gossip_loader = importlib.machinery.SourceFileLoader( 'Gossip', '../network/Gossip.py' )
Gossip_spec = importlib.util.spec_from_loader( 'Gossip',Gossip_loader )
Gossip = importlib.util.module_from_spec(Gossip_spec)
Gossip_spec.loader.exec_module(Gossip)


# port for this node
port = 5000
# ports for the nodes connected to this node
connected_nodes = [5010, 5020]

node = Gossip.GossipNode(port, connected_nodes)