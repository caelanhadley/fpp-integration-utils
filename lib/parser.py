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
        self.ast = ASTNode(-1, 'root', 'Root node') # root node of the AST

        self.comment_buffer = None

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
        self.print_ast()
    
    def _get_comment(self):
        result = self.comment_buffer
        self.comment_buffer = None
        return result

    def parse_node(self, data, parent:ASTNode=None, d=0):
        '''
        Recursively parse a node and its children.
        '''
        new_node = ASTNode(parent=parent) # Note to self: if you dont explicitly set parent=parent (instead of just parent) it gets very unhappy.
        node_type = None
        print(data)
        if isinstance(data, dict):
            # Check if there are multiple members
            if NAME in data:
                parent.name = data.get(NAME)
            if DATA in data:
                print(f'DATA: {data.get(DATA)} - {parent}')
                for member in data.get(DATA):
                    if member == NAME:
                        parent.name = data.get(DATA).get(NAME)
                    else:
                        self.parse_node(data.get(DATA).get(member), parent, d)
            elif MEMBERS in data:
                for member in data.get(MEMBERS):
                    self.parse_node(member, parent, d)
            elif NODE in data:
                print(f'NODE: {data.get(NODE)} - {parent}')
                self.parse_node(data[NODE], parent, d) # If we are a node lets just pass the data and not register ourselfs
            elif GENERAL in data:
                for member in data.get(GENERAL):
                    if member == NAME:
                        parent.name = data.get(GENERAL).get(NAME)
                    elif member == SIZE:
                        parent.size = data.get(GENERAL).get(SIZE)
                    else:
                        self.parse_node(data[GENERAL].get(member), parent, d)
            elif SPECIAL in data:
                for member in data.get(SPECIAL):
                    if member == NAME:
                        parent.name = data.get(SPECIAL).get(NAME)
                    elif member == INPUTKIND:
                        parent.kind = INPUTKIND
                    elif member == PRIORITY:
                        parent.priority = data.get(SPECIAL).get(PRIORITY)
                    elif member == QUEUEFULL:
                        parent.queueBehavior = data.get(SPECIAL).get(QUEUEFULL)
                    else:
                        self.parse_node(data.get(SPECIAL).get(member), parent, d)
            elif KIND in data:
                self.parse_node(data.get(KIND), parent, d)
            elif INPUTKIND in data:
                parent.kind = INPUTKIND
            elif ASTNODE in data:
                # print(f'ASTNODE: {data.get(ASTNODE)}')
                for member in data[ASTNODE]:
                    print(f'MEMBER: {member}')
                    if member == NAME:
                        parent.name = data[ASTNODE].get(NAME)
                    if member == ID:
                        parent.id = data[ASTNODE].get(ID)
                        line, column = self.map.get(str(parent.id)).get('pos').split('.')
                        parent.line = line
                        parent.column = column
                        parent.src_file = self.map.get(str(parent.id)).get('file')
                    else:
                        self.parse_node(data.get(ASTNODE).get(member), parent, d)
            elif SIZE in data:
                parent.size = data.get(SIZE)
            elif PRIORITY in data:
                parent.priority = data.get(PRIORITY)
            elif SOME in data:
                for member in data[SOME]:
                    self.parse_node(data[SOME].get(member), parent, d)
            elif UNQUALIFIED in data:
                for member in data[UNQUALIFIED]:
                    if member == NAME:
                        parent.kind = data[UNQUALIFIED].get(NAME)
            elif QUEUEFULL in data:
                parent.queueBehavior = QUEUEFULL
            elif ABSTRACT_TYPE in data:
                parent.type = ABSTRACT_TYPE
            elif COMPONENT in data:
                iprint(d, "[NEW COMPONENT]")
                new_node.type = COMPONENT
                parent.add_child(new_node)
                new_node.description = self._get_comment()
                self.parse_node(data[COMPONENT], new_node, d+1)
            elif MODULE in data:
                iprint(d, "[NEW MODULE]")
                new_node.type = MODULE
                parent.add_child(new_node)
                new_node.description = self._get_comment()
                self.parse_node(data[MODULE], new_node, d+1)
            elif PORT in data:
                for member in data[PORT]:
                    new_node.type = PORT
                    parent.add_child(new_node)
                    new_node.description = self._get_comment()
                    self.parse_node(data[PORT].get(member), parent, d)
            elif SPECPORT in data:
                # iprint(d, "[NEW SPECPORT]")
                new_node.type = SPECPORT
                parent.add_child(new_node)
                new_node.description = self._get_comment()
                self.parse_node(data[SPECPORT], new_node, d+1)
            elif EVENTSPEC in data:
                new_node.type = EVENTSPEC
                parent.add_child(new_node)
                new_node.description = self._get_comment()
                self.parse_node(data[EVENTSPEC], new_node, d+1)
            elif TELEMCHSPEC in data:
                new_node.type = TELEMCHSPEC
                parent.add_child(new_node)
                new_node.description = self._get_comment()
                self.parse_node(data[TELEMCHSPEC], new_node, d+1)
            elif COMMANDSPEC in data:
                new_node.type = COMMANDSPEC
                parent.add_child(new_node)
                new_node.description = self._get_comment()
                self.parse_node(data[COMMANDSPEC], new_node, d+1)
            elif OUTPUT in data:
                parent.kind = OUTPUT
            elif ENUM in data:
                parent.type = ENUM
            elif ASYNCINPUT in data:
                parent.type = ASYNCINPUT
            elif COMMANDRECV in data:
                parent.type = COMMANDRECV
            elif COMMANDREG in data:
                parent.type = COMMANDREG
            elif COMMANDRESP in data:
                parent.type = COMMANDRESP
            elif EVENT in data:
                parent.type = EVENT
            elif TELEMETRY in data:
                parent.type = TELEMETRY
            elif TEXTEVENT in data:
                parent.type = TEXTEVENT
            elif TIMEGET in data:
                parent.type = TIMEGET
            elif ASYNC in data:
                parent.type = ASYNC
            # This next bit works for now but is not a good long term solution
            if node_type:
                new_node.type = node_type
                parent.add_child(new_node)
                new_node.description = self._get_comment()
                self.parse_node(data[node_type], new_node, d)
                iprint(d, str(new_node))
        elif isinstance(data, list):
            for member in data:
                # Check to see if the member is just a string, if so it is a comment that we need to add to the comment buffer
                if isinstance(member, str):
                    print(f'Comment: {member}')
                    self.comment_buffer = member
                else:
                    self.parse_node(member, parent, d)
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