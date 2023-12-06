import re
from lark import Lark
from lark import Lark, Tree, Token

from FormulaTree import parse_tree, delete_unary_wrapper, delete_function, simplify
from FormulaTree import Formula, AtomicArgument

def print_tree(tree, indent=0):
    if isinstance(tree, Token):
        print(" " * indent + f"{tree.type}: {tree.value}")
    elif isinstance(tree, Tree):
        print(" " * indent + f"{tree.data}")
        for subtree in tree.children:
            print_tree(subtree, indent + 4)

def print_tree_to_sygus(tree):
    if isinstance(tree, Formula):
        ret = "(" + tree.function_name
        for arg in tree.arguments:
            ret = ret + " " + print_tree_to_sygus(arg)
        ret = ret + ")"
        return ret
    elif isinstance(tree, AtomicArgument):
        return tree.value

grammar_old = """
start: formula

formula: "(" function_name arguments ")"

arguments: (arg (WS arg)*)?

arg: NAME | NUMBER | BOOL | formula

!function_name: NAME | "=" | "=<>=" | "+" | "-" | "!=" | "!" | "<" | ">" | "<=" | ">=" | "$" | "%"

NUMBER: /[0-9]+/
BOOL: "true" | "false"

%import common.CNAME -> NAME
%import common.WS
%ignore WS
"""

grammar = """
start: "(" function_name arguments ")"

arguments: ((NAME | NUMBER | BOOL | start) (WS (NAME | NUMBER | BOOL | start))*)?

!function_name: NAME | "=" | "=<>=" | "+" | "-" | "!=" | "!" | "<" | ">" | "<=" | ">=" | "$" | "%"

NUMBER: /[0-9]+/
BOOL: "true" | "false"

%import common.CNAME -> NAME
%import common.WS
%ignore WS
"""

def parse_smt_to_tree(input_file_name):
    parser = Lark(grammar)

    with open(input_file_name, 'r') as input_file:
        input_text = input_file.read()


    start_marker = "; --- Sequent"
    end_marker = "(check-sat)"
    lines = input_text.split('\n')
    start_index = -1
    end_index = len(lines)

    for i, line in enumerate(lines):
        if start_marker in line:
            start_index = i
        if end_marker in line:
            end_index = i
            break

    input_text = '\n'.join(lines[start_index+1:end_index])

    #print(input_text)
    match = re.match(r'\(assert \(not (.*)\)\)$', input_text)
    if match:
        input_text = match.group(1)
        #print("String started and ended as expected.")
    else:
        print("String did not start and end as expected. Not making changes.")

    #print("Relevant input: ")    
    #print(input_text)

    #input_string = "(assert (not (and (and (= u_x (i2u (+ (u2i u_c) 1))) (wellformed heap1 (and heap1 heap2))) true)))"
    #input_string2 = "(=<>= u_x (+ 1 2))"
    #input_string2 = "(and true)"

    tree = parser.parse(input_text)
    #print(tree)
    #print(tree.pretty())
    #print_tree(tree)

    parsed_formula = parse_tree(tree)
    #print(parsed_formula.toString())


    #print(parsed_formula.function_name)  # Example of accessing function name in the root formula
    #print(parsed_formula.get_atomar_arguments())  # Example of getting literals from the root formula
    #print(parsed_formula.get_formular_arguments())  # Example of getting formulas from the root formula

    # Example of deletion of "i2u" function

    #print(f"Unwrap \"i2u\"")
    parsed_formula = delete_unary_wrapper(parsed_formula, "i2u")
    #print(parsed_formula.toString())
    #print(f"Unwrap \"u2i\"")
    parsed_formula = delete_unary_wrapper(parsed_formula, "u2i")
    #print(parsed_formula.toString())

    #print(f"Unwrap \"assert\"")
    #parsed_formula = delete_unary_wrapper(parsed_formula, "assert")
    #print(parsed_formula.toString())
    #print(f"Unwrap \"not\"")
    #parsed_formula = delete_unary_wrapper(parsed_formula, "not")
    #print(parsed_formula.toString())

    #print(f"Delete \"k_wellFormed\"")
    parsed_formula = delete_function(parsed_formula, "k_wellFormed")
    #print(parsed_formula.toString())


    #print(f"Simplify \"and\"")
    parsed_formula = simplify(parsed_formula, "and")
    #print(f"Done Simplify \"and\"")
    #print(parsed_formula)
    #print(parsed_formula.toString())
    #print("Final result: ")
    flat_string = print_tree_to_sygus(parsed_formula)
    #print(flat_string)
    
    return flat_string
    exit()


    output_file_name = input_file_name.replace('.txt', '_essence.txt')
    with open(output_file_name, 'w') as output_file:
        output_file.write(flat_string)
