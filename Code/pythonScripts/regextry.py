import re

def extract_synthesized_method_body(input_string):
    level = 0
    markers = [0]
    parts = []

    for (i,c) in enumerate(input_string):
        if c == "(":
            if level == 0:
                markers.append(i)
            level += 1
        elif c == ")":
            level -= 1
            if level == 0:
                markers.append(i+1)
    
    for m in range(len(markers)):
        if m != len(markers)-1 and markers[m] != markers[m+1]:
            parts.append(input_string[markers[m]:markers[m+1]])

    for p in parts:
        print(p)

    return parts[-1]
# Example usage
input_string = (
    "(\n(define-fun targetFunction ((x Int) (c Int)) Tuple (mkTuple (+ c 1) c))\n)"
)
print(input_string)
print("in: " + input_string[29:-3])

result = extract_synthesized_method_body(input_string[29:-3])
print("out1: " + result)