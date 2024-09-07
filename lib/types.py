class AnalysisDataStructure:
    '''
    Analysis data structure: Root object for the analysis data structure.
    '''
    def __init__(self):
        self.component_maps = {}
        self.component_instance_maps = {}
        self.dependency_file_sets = {}
        self.direct_dependency_file_sets = {}
        self.included_file_sets = {}
        self.input_file_sets = {}
        self.levels = {}
        self.location_specifier_maps = {}
        self.missing_dependency_file_sets = {}
        self.nested_scopes = {}
        self.parent_symbol_maps = {}
        self.scope_name_lists = {}
        self.symbol_scope_maps = {}
        self.topology_maps = {}
        self.type_maps = {}
        self.use_def_maps = {}
        self.use_def_matching_lists = {}
        self.use_def_symbol_sets = {}
        self.used_symbol_sets = {}
        self.value_maps = {}
        self.visited_symbol_sets = {}
    def __str__(self):
        return f"Analysis Data Structure: {self.__dict__}"

class ComponentMap:
    '''
    Component map: A map from component symbols to the corresponding components.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class ComponentInstanceMap:
    '''
    Component instance map: A map from component instance symbols to the corresponding component instances.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class DependencyFileSet:
    '''
    Dependency file set: The set of files on which the analysis transitively depends. Used to calculate the inputs to FPP analysis tools. Included files do not appear in this set.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class DirectDependencyFileSet:
    '''
    Direct dependency file set The set of files on which the analysis directly depends. Used to calculate the inputs to external build environments. Included files do appear in this set.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class IncludedFileSet:
    '''
     Included file set: The set of files included when parsing input.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class InputFileSet:
    '''
    Input file set: The set of files presented to the analyzer.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""
    
class Level:
    '''
    Level: A nonnegative integer representing the level of recursive analysis.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class LocationSpecifierMap:
    '''
    Location specifier map: A map from pairs (symbol kind, qualified name) to location specifiers. Each entry in the map represents the specified location of a symbol.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class MissingDependencyFileSet:
    '''
    Missing dependency file set: The subset of the dependency file set consisting of files that could not be opened.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class NestedScope:
    '''
    Nested scope: A nested scope object that represents the current position in a scope traversal.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class ParentSymbolMap:
    '''
    Parent symbol map: A map from symbols to their parent symbols. For example, the symbol for a constant definition appearing inside a module M is mapped to the symbol M.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class ScopeNameList:
    '''
    Scope name list: A list of unqualified names representing the enclosing scopes, with the innermost name at the head of the list. For example, inside module B where B is inside A and A is at the top level, the scope name list is [ B, A ].
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""
    
class SymbolScopeMap:
    '''
    Symbol-scope map: A map from symbols to their scopes.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class TopologyMap:
    '''
    Topology map: A map from topology symbols to the corresponding topologies.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class TypeMap:
    '''
    Type map: A map from type and constant symbols, expressions, and type names to their types.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class UseDefMap:
    '''
    Use-def map: A map from uses (expressions and qualified identifiers that refer to definitions) to the symbols representing their definitions.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class UseDefMatchingList:
    '''
    Use-def matching list: The list of use-def matchings on the current use-def path. Used during cycle analysis.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""
    
class UseDefSymbolSet:
    '''
    Use-def symbol set: The set of symbols on the current use-def path. Used during cycle analysis.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""
    
class UsedSymbolSet:
    '''
    Used symbol set: The set of symbols used. Used during code generation.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class ValueMap:
    '''
    Value map: A map from constant symbols and expressions to their values.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""

class VisitedSymbolSet:
    '''
    Visited symbol set: The set of symbols visited so far.
    '''
    def __init__(self):
        pass
    def __str__(self):
        return ""
    
# =============================== UTILITY ================================= #
class Position:
    '''
    Represents a position in the source code
    '''
    def __init__(self, line, column):
        self.line = line
        self.column = column
    def __str__(self):
        return f"({self.line},{self.column})"
    def __repr__(self):
        return self.__str__()
    
# =============================== CODE FOR AST PARSER IMPLEMENTATION ================================= #


class ASTNode:
    '''
    Represents a node in the Abstract Syntax Tree (AST)
    Serves as the base class for all AST nodes
    '''
    # Contstructor
    def __init__(self, parent=None, type=None, description=None):
        self.children = []
        self.parent = parent
        self.type = type
        self.properties = []
        self.description = description # Also serves as comment for now
        self.identifier = None
        self.position = None
    # Methods
    def add_child(self, child):
        self.children.append(child)
    def add_property(self, property):
        self.properties.append(property)
    def __str__(self) -> str:
        result = f"\u001b[32mASTNode[{self.identifier}]\u001b[0m<\u001b[34m{self.type}\u001b[0m>"
        return result
    def __repr__(self) -> str:
        return self.__str__()
    def rprint(self, depth=0, array=None):
        '''
        Print the full AST starting from the current node
        '''
        # Header
        result = ""
        if depth == 0:
            result += "\u2514" + "\u2500\u252c\u2500" + str(self) + "\n"
        else:
            if array == True:
                result += ("  " * (depth + 1)) + "\u251c"
            else:
                result += ("  " * (depth + 1)) + "\u2514"
            result += "\u2500\u252c\u2500" + str(self) + "\n"
            depth += 1
        if self.description:
            if array == True:
                result += (("  " * (depth)) + "\u2502 ") + "\u251c" + "\u2500\u2500\u2500" + f"\u001b[32mDescription\u001b[0m: \"\u001b[36m{self.description}\u001b[0m\"\n"
            else:
                result +=  ("  " * (depth + 1)) + "\u251c" + "\u2500\u2500\u2500" + f"\u001b[32mDescription\u001b[0m: \"\u001b[36m{self.description}\u001b[0m\"\n"
        if self.position:
            if array == True:
                result += (("  " * (depth)) + "\u2502 ") + "\u251c" + "\u2500\u2500\u2500" + f"\u001b[32mPosition\u001b[0m: {self.position}\n"
            else:
                result +=  ("  " * (depth + 1)) + "\u251c" + "\u2500\u2500\u2500" + f"\u001b[32mPosition\u001b[0m: {self.position}\n"
        if self.properties:
        # Properties
            if array == True:
                result += ("  " * (depth)) + "\u2502 "
            else:
                result += ("  " * (depth + 1))
            if not self.children:
                result += "\u2514"
            else:
                result += "\u251c"
            result += "\u2500\u252c\u2500" + "\u001b[32mProperties\u001b[0m:\n"
            for prop in self.properties:
                if array == True:
                    result += ("  " * (depth)) + "\u2502 "
                else:
                    result += ("  " * (depth + 1))
                # Check if there are children
                if self.children:
                    result += "\u2502 "
                else:
                    result += "  "
                # Check if this is the last property
                if prop == self.properties[-1]:
                    result += "\u2514"
                else:
                    result += "\u2502"
                # Print the property
                result += "\u2500" * 3 + str(prop) + "\n"

        # Chlidren
        if self.children:
            result += ("  " * (depth + 1)) + "\u2514" + "\u2500\u252c\u2500" + "\u001b[32mChildren\u001b[0m:\n"
            for child in self.children:
                result +=  child.rprint(depth+1, array=(child != self.children[-1]))
        return result

    def fprint(self):
        '''
        Print the full AST starting from the current node
        '''
        # Header
        result = '\u250c' + "\u2500\u2500\u2500" + str(self) + "\n"
        if self.description:
            result += "\u251c" + "\u2500\u2500\u2500" + f"\u001b[32mDescription\u001b[0m: \"\u001b[36m{self.description}\u001b[0m\"\n"
        # Properties
        result += "\u251c" + "\u2500\u252c\u2500" + "\u001b[32mProperties\u001b[0m:\n"
        for prop in self.properties:
            result += "\u2502 "
            if prop == self.properties[-1]:
                result += "\u2514"
            else:
                result += "\u2502"
            result += "\u2500" * 3 + str(prop) + "\n"
        # Chlidren
        if  self.children:
            result += "\u251c" + "\u2500\u2500\u252c" + "\u001b[32mChildren\u001b[0m:\n"
            for child in self.children:
                result += "\u2502  "
                if child == self.children[-1]:
                    result += "\u2514"
                else:
                    result += "\u2502"
                result += "\u2500" * 3 + str(child) + "\n"
        return result
        
    def ancestors(self):
        '''
        The name of ancestors of the current node, including the current node
        '''
        if not self.parent:
            return "No ancestors"
        result = ""
        current = self
        while current.parent:
            result += str(current.parent) + " -> "
            current = current.parent
        result += str(self)
        return result
        

class Property(ASTNode):
    '''
    FPP Property Object
    Used to represent any key-value pair in the AST
    '''
    def __init__(self, key, value, parent=None, description=None):
        super().__init__(parent, description)
        self.key = key
        self.value = value
    def __str__(self):
        result = ""
        if self.identifier:
            result += f"\u001b[32mProperty[{'{:4d}'.format(int(self.identifier))}] \u001b[0m<\u001b[34m{self.key}\u001b[0m: \u001b[33m{self.value}\u001b[0m>"
        else:
            result += f"\u001b[32mProperty[{'{:4}'.format('')}] \u001b[0m<\u001b[34m{self.key}\u001b[0m: \u001b[33m{self.value}\u001b[0m>"
        if self.position:
            result += f" @ {self.position}"
        return result
    def __repr__(self):
        self.__str__()

class Component(ASTNode):
    '''
    FPP Component Object
    '''
    def __init__(self, id, name, description=None):
        super().__init__(id, name, description)
        self.ports = {}
        self.special_ports = {}
        self.events = {}
        self.commands = {}
        self.parameters = {}
        self.telemetry_channels = {}
        self.containers = {}
        self.records = {}

class Port(ASTNode):
    '''
    FPP Port Object
    '''
    def __init__(self, id, name, params=None, return_type=None, description=None):
        super().__init__(id, name, description)
        self.params = params if params else []
        self.return_type = return_type

    def add_param(self, param):
        self.params.append(param)

class Enum(ASTNode):
    '''
    FPP Enum Object
    '''
    def __init__(self, id, name, description=None):
        super().__init__(id, name, description)
        self.constants = {}

    def add_constant(self, const_id, const_name, const_value=None, description=None):
        self.constants[const_id] = {
            "name": const_name,
            "value": const_value,
            "description": description
        }

class Command(ASTNode):
    '''
    FPP Command Object
    '''
    def __init__(self, id, name, description=None):
        super().__init__(id, name, description)

class Parameter(ASTNode):
    '''
    FPP Parameter
    '''
    def __init__(self, id, name, kind=None, type_name=None, description=None):
        super().__init__(id, name, description)
        self.kind = kind
        self.type_name = type_name

class TelemetryChannel(ASTNode):
    '''
    FPP Telemetry Channel Object
    '''
    def __init__(self, id, name, description=None):
        super().__init__(id, name, description)

class Container(ASTNode):
    '''
    FPP Container Object
    '''
    def __init__(self, id, name, description=None):
        super().__init__(id, name, description)

class Record(ASTNode):
    '''
    FPP Record Object
    '''
    def __init__(self, id, name, description=None):
        super().__init__(id, name, description)