from json import load as jload
from time import sleep
from lib.util import file_exists, iprint
from lib.types import *
from lib.enum import *
import os

class Parser:
    '''
    A parser for AST data.
    '''
    def __init__(self):
        self.raw = None # json data from which to compose the ast
        self.map = None
        self.ast = None # root node of the AST
        self.lastNode = None
        self.lastObject = None
        self.lastElement = None
        self.lastType = None
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
        self.ast.rprint()
    
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
    
    def _get_last_type(self):
        if self.lastType:
            result = self.lastType
            self.lastType = None
            return result
        return None
    
    def create_node(self, type, parent:ASTNode=None, depth=0):
        new_node = ASTNode(parent, type, self._get_comment())
        if not self.ast:
            self.ast = new_node
            iprint(depth, f'Created root node: {new_node}') # Could it be possible for the root node to have a comment?
        else:
            iprint(depth, f'Created node: {new_node}') # Debug
            if new_node.description:
                iprint(depth, f'Added comment: "\u001b[36m{new_node.description}\u001b[0m" to {new_node}')
            self.lastObject = new_node
        return new_node
    
    def create_property(self, key, value, parent:ASTNode=None):
        new_property = Property(key, value, parent)
        self.lastObject = new_property
        return new_property
    
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
    def register_type(self, type):
        self.lastType = type

    def parse_node(self, data, parent:ASTNode=None, d=0):
        # For debugging purposes
        if (self.ast):
            os.system('clear')
            print(self.ast.rprint())
        sleep(0.01)

        # Is the data empty?
        if not data:
            return
        
        # If the data is a string, we should add it as a property/comment
        if isinstance(data, str):
            if parent:
                if self.lastElement:
                    self.register_key(self.lastElement, parent)
                    self.register_value(data, parent)
                    iprint(d, f'Added property(a1): \u001b[34m{parent.properties[-1]}\u001b[0m to {parent}')
                    self.lastElement = None
                    return
                else:
                    # This is a comment
                    print('\u001b[36m' + data + '\u001b[0m')
                    self.register_comment(data)
                    return
            iprint(d, f'Found string: {data}')
            return
        self.lastElement = None
        if isinstance(data, int):
            iprint(d, f'Found integer: {data}')
            return
        if isinstance(data, list):
            for x in data:
                print('Element:', x)
                self.parse_node(x, parent, d+1)
            return
        for x,y in data.items():
            print('DICT:', x)
            if x in [DEFMODULE, DEFCOMPONENT, SPECPORT, SPECEVENT, SPECTELEMETRY, SPECCOMMAND, PORT]:
                print(f"FOUND {x}")
                # lets register our type and continue
                self.register_type(x)
            # If we are an ASTNODE, we should create a new node.
            if x == ASTNODE:
                # First lets make a new node
                new_node = self.create_node(self._get_last_type(), parent, d)
                if parent:
                    parent.add_child(new_node)
                self.lastNode = new_node
                # Now lets parse the contents of this node.
                for xx in y:
                    print('Element:', xx)
                    if xx == ID:
                        iprint(d, f'ID: {y[xx]}')
                        new_node.identifier = y[xx]
                        continue
                    # If our child is a string, we should add it as a property
                    if isinstance(y[xx], str):
                        new_node.add_property(Property(xx, y[xx]))
                        iprint(d, f'Added property: {new_node.properties[-1]} to {new_node}')
                        continue
                    # This is DATA which will have who knows what but everything in it should point to us
                    elif xx == DATA:
                       iprint(d, f'Parsing DATA {y[xx]}...')
                       for datum in y[xx]:
                            # Datum is the key, y[xx][datum] is the value
                            key = datum
                            value = y[xx][datum]
                            iprint(d, f'Parsing k:{key}, v:{value}...')

                            # There are some exceptional tags that we need to handle
                            if key == GENERAL:
                                for zz in value:
                                    iprint(d, f'Parsing[GENERAL] {zz}...')
                                    self.register_type(zz)
                                    self.lastElement = zz
                                    self.parse_node(value[zz], new_node, d+1)
                                continue
                            if key == KIND:
                                for zz in value:
                                    self.register_key(KIND, new_node)
                                    self.register_value(zz, new_node)
                                continue
                            
                            
                            # If the value is a string, we should add it as a property and thats all
                            if isinstance(value, str):
                                new_node.add_property(Property(key, value))
                                iprint(d, f'Added property: {new_node.properties[-1]} to {new_node}')
                                continue
                            # If the value is a dictionary
                            if isinstance(value, dict):
                                iprint(d, f'Parsing[DICT] {value} ')
                                # We need to parse its conents but we also need to temporarily store the key just in case it is a string
                                for zz in value:
                                    self.lastElement = zz
                                    self.parse_node(value[zz], new_node, d+1)
                                continue
                            # If the value is a list
                            if isinstance(value, list):
                                # Seperate the list into its elements
                                for element in value:
                                    print('Element:')  
                                    self.parse_node(element, new_node, d+1)
                                continue
                            print('Error: Unhandled data type.')
                continue
            elif x == MEMBERS:
                for xx in y:
                    iprint(d, f'Parsing member {str(xx)[:50]}...')
                    self.parse_node(xx, parent, d+1)
                continue
            # If our only chhild is a string, we should add it as a property
            elif isinstance(y, str):
                if parent:
                    parent.add_property(Property(x, y))
                    iprint(d, f'Added property: {parent.properties[-1]} to {parent}')
                    return
                else:
                    iprint(d, f'Found string: {y}')
                    return
            self.parse_node(y, parent, d+1)
            
        # iprint(d, f'Parsing {x}...')

    def print_node(self, node: ASTNode, d=0):
        '''
        Print a node and its children.
        '''
        print(node.fprint())
        for child in node.children:
            self.print_node(child, d+1)