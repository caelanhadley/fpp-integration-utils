"""
Utility functions for FPP AST parser.
"""
from os.path import exists

def file_exists(path) -> bool:
    try:
        if path and not exists(path):
            print(f'\u001b[31mERROR: File not found: {path}\u001b[0m')
        return False
    except Exception as e:
        print(f'\u001b[31mError: {e}\u001b[0m')
        return False
    return True

def iprint(depth, text, newline=True, indent=2, char=' '):
    '''
    Print text with indentation.
    '''
    print(((char*indent)*depth) + str(text), end=('\n' if newline else ''))
        