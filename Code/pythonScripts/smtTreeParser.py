import re
from lark import Lark
from lark import Lark, Tree, Token

from FormulaTree import (
    parse_tree,
    delete_unary_wrapper,
    delete_function,
    simplify_and,
    remove_cast,
    replace_fn_name,
    simplify_created,
    replace_array_access,
)
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


def cut_smt_assertion_from_file(input_file_name):
    with open(input_file_name, "r") as input_file:
        input_text = input_file.read()

    start_marker = "; --- Sequent"
    end_marker = "(check-sat)"
    lines = input_text.split("\n")
    start_index = -1
    end_index = len(lines)

    for i, line in enumerate(lines):
        if start_marker in line:
            start_index = i
        if end_marker in line:
            end_index = i
            break

    input_text = "\n".join(lines[start_index + 1 : end_index])

    match = re.match(r"\(assert \(not (.*)\)\)$", input_text)
    if match:
        input_text = match.group(1)
    else:
        print("String did not start and end as expected. Not making changes.")

    return input_text


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
start: "(" function_name? arguments ")"

arguments: ((NAME | NUMBER | BOOL | CREATED | start) (WS (NAME | NUMBER | BOOL | CREATED | start))*)?

!function_name: NAME | "=" | "=<>=" | "+" | "-" | "!=" | "!" | "<" | ">" | "<=" | ">=" | "$" | "%" | "=>"

CREATED: "|field_java.lang.Object::<created>|"
NUMBER: /[0-9]+/
BOOL: "true" | "false"

%import common.CNAME -> NAME
%import common.WS
%ignore WS
"""


def parse_smt_to_tree(smt_text):
    parser = Lark(grammar)
    tree = parser.parse(smt_text)
    # print_tree(tree)
    parsed_formula = parse_tree(tree)
    # print(parsed_formula.toString_old())
    return parsed_formula


def cleanup_tree_from_smt(parsed_formula):

    print("start: " + print_tree_to_sygus(parsed_formula))
    new_parsed_formula = delete_unary_wrapper(parsed_formula, "i2u")
    new_parsed_formula = delete_unary_wrapper(new_parsed_formula, "u2i")
    new_parsed_formula = delete_unary_wrapper(new_parsed_formula, "b2u")
    new_parsed_formula = delete_unary_wrapper(new_parsed_formula, "u2b")
    new_parsed_formula = delete_function(new_parsed_formula, "k_wellFormed")
    # print("deleting wrappers...")
    # print("done" + print_tree_to_sygus(new_parsed_formula))
    new_parsed_formula = remove_cast(new_parsed_formula, "sort_int")
    # print("after: " + print_tree_to_sygus(new_parsed_formula))
    # new_parsed_formula = simplify_created(new_parsed_formula)
    # print("after: " + print_tree_to_sygus(new_parsed_formula))
    new_parsed_formula = replace_fn_name(
        new_parsed_formula, to_replace="k_length", replace_by="seq.len"
    )
    # print("after: " + print_tree_to_sygus(new_parsed_formula))
    # print("simplified0: " + print_tree_to_sygus(new_parsed_formula))
    new_parsed_formula = simplify_created(new_parsed_formula)
    new_parsed_formula = simplify_and(new_parsed_formula)
    new_parsed_formula = replace_array_access(new_parsed_formula)
    print("\naccess modified: " + print_tree_to_sygus(new_parsed_formula))
    return new_parsed_formula
