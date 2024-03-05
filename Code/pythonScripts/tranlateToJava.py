import re


def main():
    synthesized_code_path = ".\\pythonScripts\\temp\\synthesizedCode.txt"
    try:
        with open(synthesized_code_path, "r") as synthesized_code_file:
            target_function = synthesized_code_file.read()
    except FileNotFoundError:
        print("No synthesized code. Abort...")
        return

    print("long: " + target_function)
    synthesized_method_body = extract_synthesized_method_body(target_function)
    print("short: ", synthesized_method_body)

    # code_tree = parse_smt_to_tree(synthesized_method_body)
    # print(code_tree.toString())
    # target_string = print_tree_to_sygus(code_tree)
    # print(target_string)


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


def parse_third_part_old(input_string):
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

        if not stack:
            # No open parentheses, consider it as a complete part
            parts.append(current_part.strip())
            current_part = ""

    # Filter out empty strings
    parts = list(filter(None, parts))

    return parts


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

    # Process the first part
    first_part = parse_first_part(parts[0])

    # Remove leading and trailing whitespaces for the second part
    second_part = parts[1].strip()

    # Process the third part
    third_part = [part.strip() for part in parts[2][1:-1].split()]

    print("Parts: ", [first_part, second_part, third_part])


def extract_synthesized_method_body_old(input_string):
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

    in_out_pairs = []
    variables = parts[0].removeprefix("(").removesuffix(")").split(" ")
    print("Variables: ", variables)
    print("Parts: ", parts)
    return parts[-1]


test_cases = [
    ("(mkTuple (+ c 1) c)", ["(+ c 1)", "c"]),
    ("(mkTuple (+ c (+ c 1)) c)", ["(+ c (+ c 1))", "c"]),
    ("(mkTuple (+ (+ c 1) (+ (+ c 1) 1)) c)", ["(+ (+ c 1) (+ (+ c 1) 1))", "c"]),
    ("(mkTuple (+ c (+ c 1)) c a b d)", ["(+ c (+ c 1))", "c", "a", "b", "d"]),
]


if __name__ == "__main__":
    input_str = "((x Int) (c Int) (s Seq))"
    output = parse_first_part(input_str)
    print("first: ", output)

    for input_str, expected_output in test_cases:
        result = parse_third_part(input_str)
        if not result == expected_output:
            print(
                f"Error: Expected {expected_output}, got {result} for input {input_str}"
            )
    # main()
