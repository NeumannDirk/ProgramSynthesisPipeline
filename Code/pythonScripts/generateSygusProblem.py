datatype_mapping_dict = {"int":"Int", "boolean":"Bool"}

def generate_output(variables, preconditions, postconditions):
    output = "(set-logic ALL)\n"
    output += "(declare-datatype Tuple ((empty) (mkTuple "
    
    # creating the tuple
    for (index, var) in enumerate(variables):
        output += f"(getField{str(index)} {datatype_mapping_dict[var[2]]})"
    output += ")))\n\n"
    
    # variables for conditions
    for var in variables:
        output += f"(declare-var {var[0]}_preCon {datatype_mapping_dict[var[2]]})\n"
        output += f"(declare-var {var[0]}_postCon {datatype_mapping_dict[var[2]]})\n"
    output += "\n"
    
    # Precondition and postcondition definitions
    output += "(define-fun preCondition ("
    output += ' '.join([f"({var[0]}_preCon {datatype_mapping_dict[var[2]]})" for var in variables])
    output += ") Bool "
    output += f"(and {' '.join(preconditions)}))\n\n" #TODO: Change variable names inside preconditions
    
    output += "(define-fun postCondition ("
    output += ' '.join([f"({var[0]}_postCon {datatype_mapping_dict[var[2]]})" for var in variables])
    output += ") Bool "
    output += f"(and {' '.join(postconditions)}))\n\n" #TODO: Change variable names inside postconditions
    
    # Synth-fun targetFunction definition
    output += "(synth-fun targetFunction ("
    output += ' '.join([f"({var[0]} {datatype_mapping_dict[var[2]]})" for var in variables])
    output += ") Tuple)\n\n"
    
     # variables for constraints
    for var in variables:
        output += f"(declare-var {var[0]}_in {datatype_mapping_dict[var[2]]})\n"
        output += f"(declare-var {var[0]}_out {datatype_mapping_dict[var[2]]})\n"
    output += "\n"
    
    # Constraint definition
    output += "(constraint (forall ("
    output += ' '.join([f"({var[0]}_in {datatype_mapping_dict[var[2]]}) ({var[0]}_out {datatype_mapping_dict[var[2]]})" for var in variables])
    
    output += ") "
    output += "(=>\n(and\n(preCondition "
    output += ' '.join([f"{var[0]}_in" for var in variables])
    output += ") "
    
    target_func_call = "(targetFunction " + ' '.join([f"{var[0]}_in" for var in variables]) + ")"
    
    for (index, var) in enumerate(variables):
        output += f"\n(= {var[0]}_out (getField{index} {target_func_call}))"
    
    output += ")\n(and\n(postCondition "
    output += ' '.join([f"{var[0]}_out" for var in variables])
    output += ") "
    
    for var in variables:
        if not var[1]:
            output += f"\n(= {var[0]}_in {var[0]}_out)"
    
    output += "))\n))\n(check-synth)"
    
    return output

# Example input
variables = [("x", True, "int"), ("c", False, "int"), ("d", False, "int")]
preconditions = ["(= x (+ c d))"]
postconditions = ["(= x (+ c 1))"]

output_string = generate_output(variables, preconditions, postconditions)
print(output_string)
