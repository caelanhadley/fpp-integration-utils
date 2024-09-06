from json import load as jload
from lib.util import file_exists, iprint
from lib.types import *
from lib.enum import *

class Parser:
    '''
    A parser for AST data.
    '''
    def __init__(self):
        self.raw = None # json data from which to compose the ads
        self.map = None
        self.ast = None # root node of the AST
        self.lastNode = None
        self.commentBuffer = None
        self.propertyBuffer = None

    def load(self, path):
        '''
        Load json data from a file.
        '''
        file_exists(path) # Check if the file exists
        with open(path, 'r') as file:
            self.path = path
            return jload(file)

    def parse(self, path, map):
        '''
        Parse an fpp ast json file.
        '''
        self.raw = self.load(path)
        self.map = self.load(map)
        self.parse_node(self.raw[0], self.ast)
        print('=======================================================================================================================')
        # self.print_node(self.ast)
        print(self.ast.rprint())
    
    def _get_comment(self):
        if self.commentBuffer:
            result = self.commentBuffer
            self.commentBuffer = None
            return result
        return None

    def _get_last_node(self):
        if self.lastNode:
            result = self.lastNode
            self.lastNode = None
            return result
        return None
    
    def create_node(self, type, parent:ASTNode=None, depth=0):
        new_node = ASTNode(parent, type, self._get_comment())
        if not self.ast:
            self.ast = new_node
            iprint(depth, f'Created root node: {new_node}') # Could it be possible for the root node to have a comment?
        else:
            iprint(depth, f'Created node: {new_node}   [{new_node.ancestors()}]') # Debug
            if new_node.description:
                iprint(depth, f'Added comment: "\u001b[36m{new_node.description}\u001b[0m" to {new_node}')
        return new_node
    def create_property(self, key, value, parent:ASTNode=None):
        return Property(key, value, parent)
    
    # Buffer Management
    def register_key(self, key: str, parent:ASTNode=None):
        self.propertyBuffer = self.create_property(key, None, parent)
    def register_value(self, value, parent:ASTNode=None):
        if self.propertyBuffer:
            self.propertyBuffer.value = value
            parent.add_property(self.propertyBuffer)
            self.propertyBuffer = None
        else:
            print('\u001b[31m' + 'Error: No property buffer found.' + '\u001b[0m')
            exit(1)
    def register_comment(self, comment):
        self.commentBuffer = comment

    def parse_node(self, data, parent:ASTNode=None, d=0):
        '''
        Recursively parse a node and its children.
        '''
        # Did we get any data?
        if not data:
            # iprint(d, 'No data found.')
            return

        # Is this a string?
        # Let's keep this seperate from the integers because we want to capture comments.
        if isinstance(data, str):
            if self.propertyBuffer:
                if not self.propertyBuffer.value and self.lastNode:
                    self.register_value(data, parent)
                    iprint(d, f'Added property(a0): \u001b[34m{parent.properties[-1]}\u001b[0m to {parent}')
                else:
                    self.register_value(data, parent)
                    iprint(d, f'Added property(a1): \u001b[34m{data}\u001b[0m to {parent}')
            else:
                self.register_comment(data)
                # iprint(d, f'Added comment: "\u001b[36m{data}\u001b[0m" to the buffer.')
            return
        
        # Is this an integer?
        if isinstance(data, int):
            iprint(d, f'Found Integer: {data}')
            return

        # Is this a list? If so lets go ahead and parse each element.
        if isinstance(data, list):
            for x in data:
                # iprint(d, f'Parsing list[{len(x)}]')
                self.parse_node(x, parent, d+1)
            return

        # What type of AST node is this?
        for x,y in data.items():
            # Should we create a node for this?
            if x in [DEFMODULE, DEFCOMPONENT, SPECPORT, SPECEVENT, SPECTELEMETRY]: ################################## Add more types here like port spec etc.
                # iprint(d, f'Parsing {x}...')
                node = self.create_node(x, parent, d)
                if parent:
                    parent.add_child(node)
                self.parse_node(y, node, d+1)
                return
            elif x in [DATA]:
                # The data itself can contain a string or a dictionary
                # Lets check for a string first
                if isinstance(y, str):
                    self.register_key(x, parent)
                    self.register_value(y, parent)
                    iprint(d, f'Added property(b0): \u001b[34m{parent.properties[-1]}\u001b[0m to {parent}')
                    return
                
                # If here, This must be a dictionary
                for z in y:
                    # Data might be just a string 
                    if isinstance(y[z], str):
                        self.register_key(z, parent)
                        self.register_value(y[z], parent)
                        iprint(d, f'Added property(b1): \u001b[34m{parent.properties[-1]}\u001b[0m to {parent}')
                        continue
                    self.lastNode = z
                    self.parse_node(y[z], parent, d+1)
                return
            else:
                # Case 1: We don't have any children, in this case we are the value.
                if not y:
                    # iprint(d, f'Oops, value: {x, self.lastNode}.')
                    self.register_key(self.lastNode, parent)
                    self.register_value(x, parent)
                    iprint(d, f'Added property(c): \u001b[34m{parent.properties[-1]}\u001b[0m to {parent}')
                    return
                
                # Are we itterable?
                if isinstance(y, list):
                    # iprint(d, f'Parsing list[{len(y)}]')
                    for z in y:
                        self.parse_node(z, parent, d+1)
                    return

                # Are we a dictionary?
                if isinstance(y, dict):
                    # iprint(d, f'Parsing dictionary[{len(y)}] : {x}')
                    self.lastNode = x
                    self.parse_node(y, parent, d+1)
                    return
                
                # We must be a key
                self.register_key(x, parent)
                self.parse_node(y, parent, d+1)

    def print_node(self, node:ASTNode, d=0):
        '''
        Print a node and its children.
        '''
        print(node.fprint())
        for child in node.children:
            self.print_node(child, d+1)