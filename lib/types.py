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
    


# =============================== CODE FOR AST PARSER IMPLEMENTATION ================================= #

class ASTNode:
    '''
    Represents a node in the Abstract Syntax Tree (AST)
    '''
    def __init__(self, id="", name="", description="", type="", kind="", size="", priority="", queueBehavior="", parent=None):
        self.id = id
        self.name = name
        self.description = description
        self.children = []
        self.parent = parent
        self.type = type
        self.kind = kind
        self.size = size
        self.priority = priority
        self.queueBehavior = queueBehavior
        self.line = None
        self.column = None
        self.src_file = None
    def add_child(self, child):
        self.children.append(child)
    def __str__(self):
        result = f"[{self.id}] {self.name}"
        last_prop = None
        if self.description:
            result += f"\u001b[2m ({self.description})\u001b[0m"
        if self.type and self.type != "None":
            last_prop = f"type: {self.type}"
        if self.kind and self.kind != "None":
            if last_prop: result += "\n\t\u2523\u2501 " + last_prop
            last_prop = f"kind: {self.kind}"
        if self.size and self.size != "None":
            if last_prop: result += "\n\t\u2523\u2501 " + last_prop
            last_prop = f"size: {self.size}"
        if self.priority and self.priority != "None":
            if last_prop: result += "\n\t\u2523\u2501 " + last_prop
            last_prop = f"priority: {self.priority}"
        if self.queueBehavior and self.queueBehavior != "None":
            if last_prop: result += "\n\t\u2523\u2501 " + last_prop
            last_prop = f"queue behvaior: {self.queueBehavior}"
        if self.line and self.column:
            if last_prop: result += "\n\t\u2523\u2501 " + last_prop
            last_prop = f"line: {self.line}, column: {self.column}"
        if self.src_file:
            if last_prop: result += "\n\t\u2523\u2501 " + last_prop
            last_prop = f"src: {self.src_file}"
        if last_prop: result += "\n\t\u2517\u2501 " + last_prop
        result += "\u001b[0m"
        return result
    def __repr__(self):
        return self.__str__()
    
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