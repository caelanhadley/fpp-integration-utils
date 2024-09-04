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
        # self.print_ast()
    
    def _get_comment(self):
        result = self.commentBuffer
        self.commentBuffer = None
        return result
    
    def create_node(self, type, parent:ASTNode=None):
        return ASTNode(parent, type)
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
    def register_comment(self, parent:ASTNode, comment):
        parent.description = comment

    def parse_node(self, data, parent:ASTNode=None, d=0):
        '''
        Recursively parse a node and its children.
        '''
        input()
        # Did we get any data?
        if not data:
            iprint(d, 'No data found.')
            return

        # Is this a string?
        # Let's keep this seperate from the integers because we want to capture comments.
        if isinstance(data, str):
            if self.propertyBuffer:
                self.register_value(data, parent)
                iprint(d, f'Added property: \u001b[34m{data}\u001b[0m to {parent}')
            else:
                self.register_comment(parent, data)
                iprint(d, f'Added comment: "\u001b[36m{data}\u001b[0m" to {parent}')
            return
        
        # Is this an integer?
        if isinstance(data, int):
            iprint(d, f'Found Integer: {data}')
            return

        # Is this a list? If so lets go ahead and parse each element.
        if isinstance(data, list):
            for x in data:
                iprint(d, f'Parsing list[{len(x)}]')
                self.parse_node(x, parent, d+1)
            return

        # What type of AST node is this?
        for x,y in data.items():
            # Should we create a node for this?
            if x in [DEFMODULE, DEFCOMPONENT]:
                iprint(d, f'Parsing {x}...')
                node = self.create_node(x, parent)
                print(f'Created node: {node}\n\t{node.ancestors()}') # Debug
                if parent:
                    parent.add_child(node)
                self.parse_node(y, node, d+1)
                return
            elif x in [DATA]:
                for z in y:
                    # Data might be just a string 
                    if isinstance(y[z], str):
                        self.register_key(z, parent)
                        self.register_value(y[z], parent)
                        iprint(d, f'Added property: \u001b[34m{parent.properties[-1]}\u001b[0m to {parent}')
                        continue
                    self.parse_node(y[z], parent, d+1)
                return
            else:
                # Case 1: We don't have any children, in this case we are the value.
                if not y:
                    iprint(d, f'Oops, value: {x, self.lastNode}.')
                    self.register_key(self.lastNode, parent)
                    self.register_value(x, parent)
                    iprint(d, f'Added property: \u001b[34m{parent.properties[-1]}\u001b[0m to {parent}')
                    return
                
                # Are we itterable?
                if isinstance(y, list):
                    iprint(d, f'Parsing list[{len(y)}]')
                    for z in y:
                        self.parse_node(z, parent, d+1)
                    return

                # Are we a dictionary?
                if isinstance(y, dict):
                    iprint(d, f'Parsing dictionary[{len(y)}] : {x}')
                    self.lastNode = x
                    self.parse_node(y, parent, d+1)
                    return
                
                # We must be a key
                self.register_key(x, parent)
                self.parse_node(y, parent, d+1)

        
    def print_ast(self):
        '''
        Print the AST.
        '''
        self.print_node(self.ast)
    
    def print_node(self, node, d=0):
        '''
        Print a node and its children.
        '''
        iprint(d, node)
        for child in node.children:
            self.print_node(child, d+1)