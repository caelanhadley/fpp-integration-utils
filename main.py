#!/usr/bin/python3

"""
This script is used to parse the AST json file and extract useful information
"""
import argparse
from lib.parser import Parser

if __name__ == '__main__':
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='Data Parser')
    parser.add_argument('path', type=str, help='Path to AST json file')
    parser.add_argument('map', type=str, help='Path to loc map json file')
    parser.add_argument('--out', '-o', type=str, help='Output directory')
    args = parser.parse_args()
    path = args.path
    map = args.map
    out = args.out
    ast_parser = Parser().parse(path, map)