import re

datatype_mapping_dict = {"int": "Int", "boolean": "Bool", "int[]": "(Seq Int)"}


def replace_varname(replace_in, replace_what, replace_with):
    pattern = r"\b" + re.escape(replace_what) + r"\b"
    result = re.sub(pattern, replace_with, replace_in)
    return result


def generate_sygus_problem_old(variables, preconditions, postconditions, grammar=None):
    output = "(set-logic ALL)\n"
    output += "(declare-datatype Tuple ((empty) (mkTuple "

    # creating the tuple
    for index, var in enumerate(variables):
        output += f"(getField{str(index)} {datatype_mapping_dict[var[2]]})"
    output += ")))\n\n"

    # variables for conditions
    for var in variables:
        output += f"(declare-var {var[0]}_preCon {datatype_mapping_dict[var[2]]})\n"
        output += f"(declare-var {var[0]}_postCon {datatype_mapping_dict[var[2]]})\n"
    output += "\n"

    # Precondition and postcondition definitions
    edited_precondition = " ".join(preconditions)
    edited_postcondition = " ".join(postconditions)
    for var in variables:
        edited_precondition = replace_varname(
            edited_precondition, var[0], var[0] + "_preCon"
        )  # edited_precondition.replace(var[0], var[0] + "_preCon")
        edited_postcondition = replace_varname(
            edited_postcondition, var[0], var[0] + "_postCon"
        )  # edited_postcondition.replace(var[0], var[0] + "_postCon")

    output += "(define-fun preCondition ("
    output += " ".join(
        [f"({var[0]}_preCon {datatype_mapping_dict[var[2]]})" for var in variables]
    )
    output += ") Bool "
    output += f"(and {edited_precondition}))\n\n"  # TODO: Change variable names inside preconditions

    output += "(define-fun postCondition ("
    output += " ".join(
        [f"({var[0]}_postCon {datatype_mapping_dict[var[2]]})" for var in variables]
    )
    output += ") Bool "
    output += f"(and {edited_postcondition}))\n\n"  # TODO: Change variable names inside postconditions

    # Synth-fun targetFunction definition
    output += "(synth-fun targetFunction ("
    output += " ".join(
        [f"({var[0]} {datatype_mapping_dict[var[2]]})" for var in variables]
    )
    output += ") Tuple)\n\n"

    # variables for constraints
    for var in variables:
        output += f"(declare-var {var[0]}_in {datatype_mapping_dict[var[2]]})\n"
        output += f"(declare-var {var[0]}_out {datatype_mapping_dict[var[2]]})\n"
    output += "\n"

    # Constraint definition
    output += "(constraint (forall ("
    output += " ".join(
        [
            f"({var[0]}_in {datatype_mapping_dict[var[2]]}) ({var[0]}_out {datatype_mapping_dict[var[2]]})"
            for var in variables
        ]
    )

    output += ") "
    output += "(=>\n\t(and\n\t\t(preCondition "
    output += " ".join([f"{var[0]}_in" for var in variables])
    output += ")"

    target_func_call = (
        "(targetFunction " + " ".join([f"{var[0]}_in" for var in variables]) + ")"
    )

    for index, var in enumerate(variables):
        output += f"\n\t\t(= {var[0]}_out (getField{index} {target_func_call}))"

    output += "\n\t)\n\t(and\n\t\t(postCondition "
    output += " ".join([f"{var[0]}_out" for var in variables])
    output += ")"

    for var in variables:
        if not var[1]:
            output += f"\n\t\t(= {var[0]}_in {var[0]}_out)"

    output += "\n\t)\n)))\n(check-synth)"

    return output


def generate_sygus_problem(
    variables, preconditions, postconditions, loopVariantVar=None, grammar=None
):
    mod_vars = [(_n, _mod, _t) for (_n, _mod, _t) in variables if _mod]
    con_vars = [(_n, _mod, _t) for (_n, _mod, _t) in variables if not _mod]

    output = "(set-logic ALL)\n"
    output += "(declare-datatype Tuple ((empty) (mkTuple "

    # creating the tuple
    for index, var in enumerate(mod_vars):
        output += f"(getField{str(index)} {datatype_mapping_dict[var[2]]})"
    output += ")))\n\n"

    # variables for conditions
    for var in variables:
        output += f"(declare-var {var[0]}_preCon {datatype_mapping_dict[var[2]]})\n"
        output += f"(declare-var {var[0]}_postCon {datatype_mapping_dict[var[2]]})\n"
    if loopVariantVar:
        output += f"(declare-var {loopVariantVar} Int)\n"
    output += "\n"

    # Precondition and postcondition definitions
    edited_precondition = " ".join(preconditions)
    edited_postcondition = " ".join(postconditions)
    for var in variables:
        edited_precondition = replace_varname(
            edited_precondition, var[0], var[0] + "_preCon"
        )  # edited_precondition.replace(var[0], var[0] + "_preCon")
        edited_postcondition = replace_varname(
            edited_postcondition, var[0], var[0] + "_postCon"
        )  # edited_postcondition.replace(var[0], var[0] + "_postCon")

    output += "(define-fun preCondition ("
    output += " ".join(
        [f"({var[0]}_preCon {datatype_mapping_dict[var[2]]})" for var in variables]
    )
    if loopVariantVar:
        output += f" ({loopVariantVar} Int)"
    output += ") Bool "
    output += f"(and {edited_precondition}))\n\n"

    output += "(define-fun postCondition ("
    output += " ".join(
        [f"({var[0]}_postCon {datatype_mapping_dict[var[2]]})" for var in variables]
    )
    if loopVariantVar:
        output += f" ({loopVariantVar} Int)"
    output += ") Bool "
    output += f"(and {edited_postcondition}))\n\n"

    # Synth-fun targetFunction definition
    output += "(synth-fun targetFunction ("
    output += " ".join(
        [f"({var[0]} {datatype_mapping_dict[var[2]]})" for var in variables]
    )
    output += ") Tuple)\n\n"

    # variables for constraints
    for var in variables:
        output += f"(declare-var {var[0]}_in {datatype_mapping_dict[var[2]]})\n"
    for var in mod_vars:
        output += f"(declare-var {var[0]}_out {datatype_mapping_dict[var[2]]})\n"
    output += "\n"

    # Constraint definition
    output += "(constraint (forall ("
    for i, var in enumerate(variables):
        if i > 0:
            output += " "
        output += f"({var[0]}_in {datatype_mapping_dict[var[2]]})"
    for var in mod_vars:
        output += f" ({var[0]}_out {datatype_mapping_dict[var[2]]})"

    if loopVariantVar:
        output += f" ({loopVariantVar} Int)"

    # output += " ".join(
    #    [
    #        f"({var[0]}_in {datatype_mapping_dict[var[2]]}) ({var[0]}_out {datatype_mapping_dict[var[2]]})"
    #        for var in variables
    #    ]
    # )

    output += ") "
    output += "(=>\n\t(and\n\t\t(preCondition "
    output += " ".join([f"{var[0]}_in" for var in variables])
    if loopVariantVar:
        output += f" {loopVariantVar}"
    output += ")"

    target_func_call = (
        "(targetFunction " + " ".join([f"{var[0]}_in" for var in variables]) + ")"
    )

    for index, var in enumerate(mod_vars):
        output += f"\n\t\t(= {var[0]}_out (getField{index} {target_func_call}))"

    output += "\n\t)\n\t(and\n\t\t(postCondition"
    for _n, _m, _ in variables:
        if _m:
            output += f" {_n}_out"
        else:
            output += f" {_n}_in"
    # output += " ".join([f"{_n}{"_out" if _m else "_in"}" for (_n, _m, _) in variables])
    if loopVariantVar:
        output += f" {loopVariantVar}"
    output += ")"

    # for var in variables:
    #    if not var[1]:
    #        output += f"\n\t\t(= {var[0]}_in {var[0]}_out)"

    output += "\n\t)\n)))\n(check-synth)"

    return output


if __name__ == "__main__":
    # Example input
    variables = [("t", True, "int"), ("c", False, "int"), ("d", False, "int")]
    preconditions = ["(= t (int.add c d))"]
    postconditions = ["(= t (int.add c 1))"]

    output_string = generate_sygus_problem(variables, preconditions, postconditions)
    print(output_string)
