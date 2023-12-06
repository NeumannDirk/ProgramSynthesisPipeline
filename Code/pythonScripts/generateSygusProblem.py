datatype_mapping_dict = {"int":"Int", "boolean":"Bool"}

def generate_sygus_problem(variables, preconditions, postconditions):
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
    edited_precondition = ' '.join(preconditions)
    edited_postcondition = ' '.join(postconditions)
    for var in variables:
        edited_precondition = edited_precondition.replace(var[0], var[0] + "_preCon")
        edited_postcondition = edited_postcondition.replace(var[0], var[0] + "_postCon")
    
    output += "(define-fun preCondition ("
    output += ' '.join([f"({var[0]}_preCon {datatype_mapping_dict[var[2]]})" for var in variables])
    output += ") Bool "
    output += f"(and {edited_precondition}))\n\n" #TODO: Change variable names inside preconditions
    
    output += "(define-fun postCondition ("
    output += ' '.join([f"({var[0]}_postCon {datatype_mapping_dict[var[2]]})" for var in variables])
    output += ") Bool "
    output += f"(and {edited_postcondition}))\n\n" #TODO: Change variable names inside postconditions
    
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
    output += "(=>\n\t(and\n\t\t(preCondition "
    output += ' '.join([f"{var[0]}_in" for var in variables])
    output += ")"
    
    target_func_call = "(targetFunction " + ' '.join([f"{var[0]}_in" for var in variables]) + ")"
    
    for (index, var) in enumerate(variables):
        output += f"\n\t\t(= {var[0]}_out (getField{index} {target_func_call}))"
    
    output += "\n\t)\n\t(and\n\t\t(postCondition "
    output += ' '.join([f"{var[0]}_out" for var in variables])
    output += ")"
    
    for var in variables:
        if not var[1]:
            output += f"\n\t\t(= {var[0]}_in {var[0]}_out)"
    
    output += "\n\t)\n)))\n(check-synth)"
    
    return output

if __name__ == "__main__":
    # Example input
    variables = [("x", True, "int"), ("c", False, "int"), ("d", False, "int")]
    preconditions = ["(= x (+ c d))"]
    postconditions = ["(= x (+ c 1))"]

    output_string = generate_sygus_problem(variables, preconditions, postconditions)
    print(output_string)
