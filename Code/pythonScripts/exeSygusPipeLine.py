from splitProblemDefinition import split_problem_definition
from readVariablesFromCorcModel import read_vars_from_corc_model
from keyRunner import run_key
from smtTreeParser import *
from generateSygusProblem import generate_sygus_problem
from Cvc5Runner import run_cvc5
import shutil
from FormulaTree import *
import os
import time
from pprint import pprint
from translateToJava import translate_synthesized_code_to_java

# corc_problem_folder = "D:\\workspaces\\runtime-EclipseApplication\\de.tu_bs.cs.isf.corc.examples\\src\\diagrams\\"
# corc_name = "maxElement"
# cbc_suffix = ".cbcmodel"
# statement_id = "542948eb-3277-4648-84a1-10aa21959227"
# str_statement = "Statement"
# corc_input_nr = "5"
# str_key = ".key"

sygus_output_file = "synthesizedCode.txt"


def setup_synthesis_structure(info, project_folder, temp_folder):
    # create temp folder
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # copy files
    shutil.copyfile(
        src=project_folder + info["statement_file"] + ".key",
        dst=temp_folder + info["statement_file"] + ".key",
    )
    shutil.copyfile(src=project_folder + "helper.key", dst=temp_folder + "helper.key")


def execute_sygus_pipeline(info):
    info["timestamps"].append(time.time())

    # setup folder structure
    project_folder = info["src_dir"] + "prove" + info["project"] + "\\"
    temp_folder = project_folder + "temp_" + info["statement_file"] + "\\"
    setup_synthesis_structure(
        info=info, project_folder=project_folder, temp_folder=temp_folder
    )
    info["timestamps"].append(time.time())

    # split problem into pre and post condition
    split_out_pre = temp_folder + info["statement_file"] + "_pre_gen.key"
    split_out_post = temp_folder + info["statement_file"] + "_post_gen.key"
    split_problem_definition(info, split_out_pre, split_out_post)
    info["timestamps"].append(time.time())

    # run KeY to translate to SMT
    key_file = ".\\pythonScripts\\key-2.13.0-exe.jar"
    run_key(key_file, split_out_pre, temp_folder)
    info["timestamps"].append(time.time())
    run_key(key_file, split_out_post, temp_folder)
    info["timestamps"].append(time.time())

    # Parse SMT conditions to Tree
    key_out_suffix = "_goal_0.smt2"

    smt_pre_cond = cut_smt_assertion_from_file(split_out_pre + key_out_suffix)
    pre_cond_formula_tree = parse_smt_to_tree(smt_pre_cond)
    pre_cond_formula_tree = cleanup_tree_from_smt(pre_cond_formula_tree)
    parsed_pre_cond = print_tree_to_sygus(pre_cond_formula_tree).replace("u_", "")

    smt_post_cond = cut_smt_assertion_from_file(split_out_post + key_out_suffix)
    post_cond_formula_tree = parse_smt_to_tree(smt_post_cond)
    post_cond_formula_tree = cleanup_tree_from_smt(post_cond_formula_tree)
    parsed_post_cond = print_tree_to_sygus(post_cond_formula_tree).replace("u_", "")

    # Get variable from cbcmodel
    variables = read_vars_from_corc_model(info["cbcmodel_path"], info["cbc_id"])

    pprint(variables)

    for i, (name, mod, type) in enumerate(variables):
        if name not in info["modifiable"]:
            variables[i] = (name, False, type)

    pprint(variables)

    if any([m for (n, m, t) in variables]):

        # print("Variables: " + str(variables))
        # print("pre: " + parsed_pre_cond)
        # print("post: " + parsed_post_cond)
        info["timestamps"].append(time.time())

        # Generate Sygus Problem
        sygus_problem = generate_sygus_problem(
            variables, [parsed_pre_cond], [parsed_post_cond]
        )
        # print("\nSyGuS Problem:\n" + sygus_problem)
        info["timestamps"].append(time.time())

        sygus_file = "sygus_gen.sy"
        with open(temp_folder + sygus_file, "w") as output_file:
            output_file.write(sygus_problem)

        # Execute cvc5
        # print("\nSyGuS Result:\n" + sygus_problem)
        info["timestamps"].append(time.time())
        run_cvc5(temp_folder + sygus_file, temp_folder + sygus_output_file)
        info["timestamps"].append(time.time())

        java_codeblock = translate_synthesized_code_to_java(
            synthesized_code_path=temp_folder + sygus_output_file,
            variable_modifiability_dict=variables,
        )
        info["timestamps"].append(time.time())
        print(info["statement_path"], "   result: ", java_codeblock)
        print("time: ", [t - info["timestamps"][0] for t in info["timestamps"]])
    else:
        print(info["statement_path"], "   result: ", ";")
        print("time: ", [t - info["timestamps"][0] for t in info["timestamps"]])
    return


def extract_synthesized_method_body(input_string):
    shortened_input = input_string.removeprefix(
        "(\n(define-fun targetFunction "
    ).removesuffix(")\n)")
    level = 0
    markers = [0]
    parts = []

    for i, c in enumerate(shortened_input):
        if c == "(":
            if level == 0:
                markers.append(i)
            level += 1
        elif c == ")":
            level -= 1
            if level == 0:
                markers.append(i + 1)

    for m in range(len(markers)):
        if m != len(markers) - 1 and markers[m] != markers[m + 1]:
            parts.append(shortened_input[markers[m] : markers[m + 1]])

    return parts[-1]


if __name__ == "__main__":
    my_info = {
        "src_dir": "D:\\evalData\\",
        "project": "maxElement",
        "statement_file": "Statement5",
        "statement_path": "D:\\evalData\\provemaxElement\\Statement5.key",
        "cbcmodel_path": "D:\\evalData\\maxElement.cbcmodel",
        "cbc_id": "ccde479c-9742-4796-b71f-c8280ee84b02",
        "result": None,
        "timestamps": [],
    }
    variables = read_vars_from_corc_model(my_info["cbcmodel_path"], my_info["cbc_id"])
    print("done")
    # execute_sygus_pipeline(my_info)
