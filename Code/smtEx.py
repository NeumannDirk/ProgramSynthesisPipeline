from lark import Lark
from lark import Lark, Tree, Token

def print_tree(tree, indent=0):
    if isinstance(tree, Token):
        print(" " * indent + f"{tree.type}: {tree.value}")
    elif isinstance(tree, Tree):
        print(" " * indent + f"{tree.data}")
        for subtree in tree.children:
            print_tree(subtree, indent + 4)

grammar = """
start: formula

formula: "(" (function_name | NAME) arguments ")"

arguments: (arg (WS arg)*)?

arg: NAME | NUMBER | BOOL | formula

function_name: "=" | "+" | "-" | "!=" | "!" | "<" | ">" | "<=" | ">=" | "$" | "%"

NUMBER: /[0-9]+/
BOOL: "true" | "false"

%import common.CNAME -> NAME
%import common.WS
%ignore WS
"""

parser = Lark(grammar)

input_string = "(assert (not (= u_x (i2u (+ (u2i u_c) 1)))))"

tree = parser.parse(input_string)
print(tree)
print_tree(tree)
