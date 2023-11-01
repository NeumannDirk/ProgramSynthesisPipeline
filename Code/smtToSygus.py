import re

def deleteFromSMTLIB(text, toDelete):
    # Step 2: Delete all occurrences of "toDelete" and their corresponding closing brackets
    # Use a stack to keep track of open and close brackets
    stack = []
    result = text
    
    while result.find(toDelete) != -1:
        print("still there at " + str(result.find(toDelete)))
        start = result.find('(' + toDelete)
        end = start + 1 + len(toDelete)
        stack = 1
        print("start: " + str(start))
        while end < len(result):
            if result[end] == '(':
                stack += 1
            elif result[end] == ')':
                stack -= 1
            if stack == 0:
                print("found at " + str(end))
                break
            end += 1
            #print("end: " + str(end))
        result = result[:start] + result[start+1+len(toDelete):end] + result[end+1:]
        result = re.sub(r' {2,}', ' ', result)
        print(result)	
    return result

# Read input from a file
input_file_name = "SMT1_pre.txt"
with open(input_file_name, 'r') as input_file:
    input_text = input_file.read()


# Step 1: Select the lines of interest between "; --- Sequent" and "(check-sat)"
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

# Join the selected lines to form the input_text
input_text = '\n'.join(lines[start_index+1:end_index])

# Step 2: Remove the leading and trailing parts
print(input_text)
match = re.match(r'\(assert \(not (.*)\)\)$', input_text)
if match:
    input_text = match.group(1)
    print("String started and ended as expected.")
else:
    print("String did not start and end as expected. Not making changes.")
print(input_text)

# Define the text to delete
deletions = ['i2u', 'u2i']

# Perform the deletion
next_iteration = input_text
for deletion in deletions:
    next_iteration = deleteFromSMTLIB(next_iteration, deletion)

# Define the output file name
output_file_name = input_file_name.replace('.txt', '_essence.txt')

# Save the result to a new file
with open(output_file_name, 'w') as output_file:
    output_file.write(next_iteration)
