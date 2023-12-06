from splitProblemDefinition import split_problem_definition
from readVariablesFromCorcModel import read_vars_from_corc_model
from keyRunner import run_key
from smtTreeParser import parse_smt_to_tree
from generateSygusProblem import generate_sygus_problem
from Cvc5Runner import run_cvc5

import shutil

corc_problem_folder = ".\\..\\..\\ExampleProblemDefinitions\\xPlusOne\\"
temp_folder = "temp\\"

corc = "newDiagram.cbcmodel"
statement_id = "4057a6e8-c7a5-4d44-82df-8f3b3d459ccd"
str_proveNewDiagram_folder = "proveNewDiagram\\"
str_statement = "Statement"
corc_input_nr = "1"
str_key = ".key"

# Get variable from cbcmodel
variables = read_vars_from_corc_model(corc_problem_folder + corc, statement_id)


pre_cond_suffix = "_pre_gen.key"
post_cond_suffix = "_post_gen.key"

#split problem into pre and post condition
split_in = corc_problem_folder + str_proveNewDiagram_folder + str_statement + corc_input_nr + str_key
split_out_pre = temp_folder + str_statement + corc_input_nr + pre_cond_suffix
split_out_post = temp_folder + str_statement + corc_input_nr + post_cond_suffix

split_problem_definition(split_in, split_out_pre, split_out_post)


#run KeY to translate to SMT
shutil.copyfile(corc_problem_folder + str_proveNewDiagram_folder + "helper.key", temp_folder + "helper.key")
key_file = "key-2.13.0-exe.jar"

run_key(key_file, split_out_pre, temp_folder)
run_key(key_file, split_out_post, temp_folder)

key_out_suffix = "_goal_0.smt2"
# Parse SMT conditions to Tree
parsed_pre_cond = parse_smt_to_tree(split_out_pre + key_out_suffix).replace("u_", "")
parsed_post_cond = parse_smt_to_tree(split_out_post + key_out_suffix).replace("u_", "")

print("Variables: " + str(variables))
print("pre: " + parsed_pre_cond)
print("post: " + parsed_post_cond)

# Generate Sygus Problem
sygus_problem = generate_sygus_problem(variables, parsed_pre_cond, parsed_post_cond)
#print("\nSyGuS Problem:\n" + sygus_problem)

sygus_file = "sygus_gen.sy"
with open(temp_folder + sygus_file, 'w') as output_file:
        output_file.write(sygus_problem)

# Execute cvc5
#print("\nSyGuS Result:\n" + sygus_problem)
sygus_output_file = "synthesizedCode.txt"
run_cvc5(temp_folder + sygus_file, temp_folder + sygus_output_file)

with open(temp_folder + sygus_output_file, 'r') as synthesized_code_file:
        target_function = synthesized_code_file.read()
print(target_function)






        
        
        
        
        
        
        
        
        
        
        
