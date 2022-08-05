import os
import json
from flask import current_app

def get_root_node():
    config_path = os.path.join( current_app.instance_path, 'config.json' )
    with open( config_path ) as pFile: config = json.load( pFile )
    root = config.get( 'root', None )
    if root:
        rootNode = Node( 'root', root )
        return rootNode
    else:
        return None

def get_categories():
    node = get_root_node()
    nodes = node.dump()
    nodes.pop( 0 )
    categories = [ x.node for x in nodes ]
    return categories


class Node:
    def __init__(self, node:str, item:dict | None = None, parent = None, root = None, depth = 0 ):
        self.data = []
        self.node = node
        self.item = item
        self.parent = parent
        self.depth = depth
        if root == None: self.root = self
        else: self.root = root
        
        self.childs = []
        if item:
            for node, item in item.items():
                self.childs.append( Node( node, item, self, self.root, self.depth + 1 ) )
        
        if self.root == self:
            self._test()

    def _test(self):
        l = self.dump()
        if len(l) != len(set(l)):
            raise Exception( 'Failed to build node tree: Nodes need to be unique' )
    def __str__(self):
        map = self.node
        for child in self.childs:
            map +=  "\n" + "  " * ( self.depth + 1 ) + "↳" +  str( child )
        return map
    def __getitem__(self, key:str):
        return self.search( key )
    def unwrap(self):
        nodes = self.dump()
        return [ { 'category': node.node, 'depth': node.depth, 'data': node.data } for node in nodes ]
    def dump(self):
        node_list = [ self ]
        for child in self.childs:
            node_list += child.dump()
        return node_list
    def search(self, node:str):
        if self.node.lower() == node.lower():
            return self
        for child in self.childs:
            res = child.search( node )
            if res: return res
        return None
    def insert(self, data):
        if isinstance( data, list ):
            self.data = self.data + data
        else:
            self.data.append( data )
    def pop(self, index:int):
        return self.data.pop( index )        