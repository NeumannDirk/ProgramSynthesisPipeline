import re

def extract_post_condition(problem_text):
    # Use regular expressions to remove the post-condition code within pointy brackets
    flat_problem_text = problem_text.replace('\n', '')
    result = re.sub(r'\\<\{.*?\}\\>', '', flat_problem_text)
    result_wo_whitespaces = re.sub(r' {2,}', ' ', result)
    #print("Text Input:")
    #print(flat_problem_text)
    #print("Modified Post-Condition:")
    #print(result_wo_whitespaces)
    return result_wo_whitespaces

def split_problem_definition(input_filename, output_pre_filename, output_post_filename):

    with open(input_filename, "r") as input_file:
        input_content = input_file.read()

    input_content = input_content.split("\\proof {")[0]

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

    problem_parts = problem_part.split("->")

    pre_copy = input_content.replace(problem_part, problem_parts[0].strip() + "}")
    pre_copy += "\n\n\\proofScript \"macro 'simp-upd';\""

    post_copy = input_content.replace(problem_part, "\\problem {" + extract_post_condition(problem_parts[1]))
    post_copy += "\n\n\\proofScript \"macro 'simp-upd';\""

    with open(output_pre_filename, "w") as output_pre_file:
        output_pre_file.write(pre_copy)

    with open(output_post_filename, "w") as output_post_file:
        output_post_file.write(post_copy)


if __name__ == "__main__":
    input_filename = "Statement1.key"
    output_pre_filename = "Statement1_pre_gen.key"
    output_post_filename = "Statement1_post_gen.key"
    split_problem_definition(input_filename, output_pre_filename, output_post_filename)