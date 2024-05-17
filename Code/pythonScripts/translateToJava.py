import re
from smtTreeParser import parse_smt_to_tree
from TreeToJavaPrinter import toJava
from itertools import cycle


def translate_synthesized_code_to_java(
    synthesized_code_path: str, variable_modifiability_dict
) -> str:
    try:
        with open(synthesized_code_path, "r") as synthesized_code_file:
            target_function = synthesized_code_file.read()
    except FileNotFoundError:
        print("No synthesized code. Abort...")
        return

    var_dict = {n: b for (n, b, _) in variable_modifiability_dict}

    synthesized_method_body = extract_synthesized_method_body(
        target_function, variable_modifiability_dict
    )

    codeblock = ""

    for n, b, t in variable_modifiability_dict:
        if b:
            codeblock += f"{t} {n}_preVersion = {n}; "

    for (name, type), statement in synthesized_method_body:
        if var_dict.get(name):
            java_code = ""
            if statement.startswith("(") and statement.endswith(")"):
                for n, b, t in variable_modifiability_dict:
                    if b:
                        statement = replace_variable_name(
                            statement, n, n + "_preVersion"
                        )
                tree = parse_smt_to_tree(statement)
                java_code = toJava(tree)
            else:
                java_code = statement
            codeblock += f"{name} = {java_code}; "

    # print("codeblock: ", codeblock)

    return codeblock


def replace_variable_name(string, old_name, new_name):
    # Construct a regular expression pattern
    pattern = r"(?<![^\W\d])" + re.escape(old_name) + r"(?![^\W\d])"
    # Use re.sub() to replace the variable name
    return re.sub(pattern, new_name, string)


def parse_first_part(input_str):
    # Remove outer brackets
    content = input_str[1:-1]

    # Use regex to extract tuples
    pattern = r"\((\w+)\s+([^)]+)\)"
    matches = re.findall(pattern, content)

    # Convert matches to list of tuples
    result = [(name, value.strip()) for name, value in matches]

    return result


def parse_third_part(input_string):
    # Remove outer brackets
    inner_content = input_string[1:-1]

    # Remove "mkTuple " (with the whitespace)
    inner_content = inner_content.replace("mkTuple ", "")

    parts = []
    current_part = ""
    stack = []

    for char in inner_content:
        if char == "(":
            stack.append("(")
        elif char == ")":
            stack.pop()

        current_part += char

        if not stack and current_part.strip():
            # No open parentheses and current_part is not empty, consider it as a complete part
            parts.append(current_part.strip())
            current_part = ""

    return parts


def extract_synthesized_method_body(input_string, variable_modifiability_dict):
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

    # Process the first part
    first_part = parse_first_part(parts[0])

    modifiable_vars = [(name) for (name, mod, _) in variable_modifiability_dict if mod]

    first_part = [
        (name, ptype) for (name, ptype) in first_part if name in modifiable_vars
    ]

    # Remove leading and trailing whitespaces for the second part
    second_part = parts[1].strip()

    # Process the third part
    third_part = parse_third_part(parts[2])

    print("Parts: ", [first_part, second_part, third_part])

    return list(zip(first_part, third_part))


if __name__ == "__main__":
    test_cases = [
        ("(mkTuple (+ c 1) c)", ["(+ c 1)", "c"]),
        ("(mkTuple (+ c (+ c 1)) c)", ["(+ c (+ c 1))", "c"]),
        ("(mkTuple (+ (+ c 1) (+ (+ c 1) 1)) c)", ["(+ (+ c 1) (+ (+ c 1) 1))", "c"]),
        ("(mkTuple (+ c (+ c 1)) c a b d)", ["(+ c (+ c 1))", "c", "a", "b", "d"]),
    ]
    main()
    input_str = "((x Int) (c Int) (s Seq))"
    output = parse_first_part(input_str)
    print("first: ", output)

    for input_str, expected_output in test_cases:
        result = parse_third_part(input_str)
        print(result)
        if not result == expected_output:
            print(
                f"Error: Expected {expected_output}, got {result} for input {input_str}"
            )
    # main()
