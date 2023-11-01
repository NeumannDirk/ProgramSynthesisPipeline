input_filename = "Statement1.key"
output_pre_filename = "Statement1_pre_gen.key"
output_post_filename = "Statement1_post_gen.key"

with open(input_filename, "r") as input_file:
    input_content = input_file.read()

# Delete the "\proof" part if it exists
input_content = input_content.split("\proof")[0]

# Find the "\problem" part
problem_start = input_content.find("\\problem")
problem_end = problem_start
depth = 0
for i in range(problem_start, len(input_content)):
    if input_content[i] == '{':
        depth += 1
    elif input_content[i] == '}':
        depth -= 1
        if depth == 0:
            problem_end = i
            break

problem_part = input_content[problem_start:problem_end + 1]

# Split the "\problem" part at the implication arrow
problem_parts = problem_part.split("->")

# Create the "_pre" copy with the first part of the logic formula
pre_copy = input_content.replace(problem_part, problem_parts[0].strip())

# Create the "_post" copy with the second part of the logic formula
post_copy = input_content.replace(problem_part, problem_parts[1].strip())

# Write the "_pre" copy to a file
with open(output_pre_filename, "w") as output_pre_file:
    output_pre_file.write(pre_copy)

# Write the "_post" copy to a file
with open(output_post_filename, "w") as output_post_file:
    output_post_file.write(post_copy)
