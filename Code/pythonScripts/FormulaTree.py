from abc import ABC, abstractmethod
from lark import Lark, Tree, Token

class AbstractArgument(ABC):
    pass

class AtomicArgument(AbstractArgument):
    def __init__(self, value):
        self.value = value

    def toString(self, indent=0):
        return f"AtomicArgument {{value:\"{self.value}\"}}\n"

class Formula(AbstractArgument):
    def __init__(self, function_name, arguments):
        self.function_name = function_name
        self.arguments = arguments

    def get_atomar_arguments(self):
        return [arg for arg in self.arguments if isinstance(arg, AtomicArgument)]
    
    def get_formular_arguments(self):
        return [arg for arg in self.arguments if isinstance(arg, Formula)]
        
    def toString_old(self, indent=0):
        output = " " * indent + f"{self.function_name}\n"
        for arg in self.arguments:
            if isinstance(arg, Formula):
                output += arg.toString(indent + 4)
            else:
                output += " " * (indent + 4) + f"{arg.value}\n"
        return output
    
    def toString(self, indent=0):
        output = " " * indent + f"Formula {{function_name:\"{self.function_name}\" arguments:[\n"
        for arg in self.arguments:
            if isinstance(arg, Formula):
                output += arg.toString(indent + 4)
            else:
                output += " " * (indent + 4) + f"AtomicArgument {{value:\"{arg.value}\"}}\n"
        output += " " * indent + "]}\n"
        return output

def parse_tree(tree):
    if isinstance(tree, Token):
        #print(f"tree.type: {tree.type}")
        if tree.type in ["RULE", "WS"]:
            return None
        else:
            return AtomicArgument(tree.value)
    elif isinstance(tree, Tree):
        #print(f"tree.data: {tree.data}")

        if tree.data == "start":
            #formula-node
            formula_node = Formula("", [])
            for child in tree.children:
                if isinstance(child, Tree):
                    if child.data == "function_name":
                        #print(str(child))
                        #print(str(child.children[0]))
                        #print(str(child.children[0].value))
                        formula_node.function_name = child.children[0].value
                    elif child.data == "arguments":
                        #print(f"child.children: {child.children}")                        
                        #print(f"child.children-class: {'Formula' if isinstance(child.children[0], Formula) else 'Token'}")
                        for arg_child in child.children:
                            #print(str(arg_child))
                            actual_arg_child = parse_tree(arg_child)
                            if actual_arg_child is not None:
                                #print(f"actual_arg_child: {actual_arg_child}")                        
                                formula_node.arguments.append(actual_arg_child)
                    else:
                        print("Found Tree with unknown data: " + str(child.data))    
                else:
                    print("Found unexpected Token-child: " + str(child))

            return formula_node

def delete_unary_wrapper(formula, wrapper_to_delete):
    if isinstance(formula, AtomicArgument):
        return AtomicArgument(formula.value)
    
    if formula.function_name == wrapper_to_delete:
        if len(formula.arguments) != 1:
            print(f"Error: The function {wrapper_to_delete} is not always unary")
            return None
        else:
            return delete_unary_wrapper(formula.arguments[0], wrapper_to_delete)
    else:
        newArgs = [delete_unary_wrapper(arg, wrapper_to_delete) for arg in formula.arguments]
        return Formula(formula.function_name, newArgs)

def delete_function(formula, function_to_delete):
    if isinstance(formula, AtomicArgument):
        return AtomicArgument(formula.value)
    
    if formula.function_name == function_to_delete:
        return None
    else:
        newArgs = []
        for arg in formula.arguments:
            newArg = delete_function(arg, function_to_delete)
            if newArg != None:
                newArgs.append(newArg)
        return Formula(formula.function_name, newArgs)
        

def simplify(formula, function_to_simplify):
    if isinstance(formula, AtomicArgument):
        return AtomicArgument(formula.value)
    
    if formula.function_name == function_to_simplify and len(formula.arguments) == 1:
        if isinstance(formula.arguments[0], AtomicArgument):
            return AtomicArgument(formula.arguments[0].value)
        else:
            return Formula(formula.arguments[0].function_name, formula.arguments[0].arguments)
    else:
        newArgs = [simplify(arg, function_to_simplify) for arg in formula.arguments]
        return Formula(formula.function_name, newArgs)