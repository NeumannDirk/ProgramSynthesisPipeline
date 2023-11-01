import re


file_name = "Statement1.key"

with open(file_name, 'r') as file:
    input_text = file.read()

program_variables_text = re.search(r'\\programVariables \{(.+?)\}', input_text, re.DOTALL).group(1)

variable_declarations = re.findall(r'(\w+)\s+(\w+);', program_variables_text)
datatypes, varnames = zip(*variable_declarations)

variables_info = []

for datatype, varname in zip(datatypes, varnames):
    variables_info.append({
        "datatype": datatype,
        "varname": varname,
        "is_unmodifiable": False
    })

for variable in variables_info:
    varname = variable['varname']
    if varname + "_old" in varnames:
        variable['is_unmodifiable'] = True
        for var in variables_info:
            if var['varname'] == varname + "_old":
                var['is_unmodifiable'] = True
                break

for variable in variables_info:
    print(f"Variable: {variable['varname']}, Datatype: {variable['datatype']}, Is Unmodifiable: {variable['is_unmodifiable']}")

unmodifiable_variables = {variable['varname'] + "_old" for variable in variables_info if variable['is_unmodifiable']}
print("\nUnmodifiable Variables:")
print(unmodifiable_variables)
